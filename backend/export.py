from typing import List
from functools import reduce

import eel
from numpy import deg2rad

from .models import data_factory
from .models import SatelliteData, ObjectData, RecipientData
from .services.intersection import IntersectionTracker, Intersections
from .core import Spacecraft, Orbit, Point, RecipientArea


last_simulation = None


class Satellite(Spacecraft):
    def __init__(self, name, cluster, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.cluster = cluster

    def __repr__(self):
        return f'Satellite({self.name})'


class ObservationObject(Point):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __repr__(self):
        return f'ObservationObject({self.name})'


class Recipient(Point):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __repr__(self):
        return f'Recipient({self.name})'


def satellite_factory(data: SatelliteData) -> Satellite:
    orbit = Orbit(
        h_p=data.perigeeAltitude,
        h_a=data.apogeeAltitude,
        i=deg2rad(data.orbitalInclination),
        omega_0=deg2rad(data.initialPerigeeArgument),
        OMEGA_0=deg2rad(data.ascendingNodeLongitude)
    )
    spacecraft = Satellite(
        name=data.name,
        cluster=data.cluster,
        gamma=deg2rad(data.opticalRotationAngle),
        y_s=deg2rad(data.sunMinimumHeightAngle),
        orbit=orbit
    )
    return spacecraft


def object_factory(data: ObjectData) -> ObservationObject:
    return ObservationObject(
        name=data.name,
        phi_=data.latitude,
        lambda_=data.longitude
    ).to_rad()


def recipient_factory(data: RecipientData) -> Recipient:
    return Recipient(
        name=data.name,
        phi_=data.latitude,
        lambda_=data.longitude
    ).to_rad()


def set_progress(time, start_time, end_time, step):
    percent = (end_time - start_time) / 100
    progress = time // percent
    if time % percent < step:
        eel.setProgress(progress + 1)


def set_settings(name, settings):
    eel.setSettings(name, [{'name': f'{el[0]}|{el[1]}'} for el in settings])


def prepare_satellites(data) -> List[Satellite]:
    satellites_data = [data_factory(el, SatelliteData) for el in data['satellites']]
    satellites = [satellite_factory(data) for data in satellites_data]
    return satellites


def prepare_objects(data) -> List[ObservationObject]:
    objects_data = [data_factory(el, ObjectData) for el in data['objects']]
    objects = [object_factory(data) for data in objects_data]
    return objects


def prepare_recipient(data) -> List[Recipient]:
    recipients_data = [data_factory(el, RecipientData) for el in data['recipients']]
    recipients = [recipient_factory(data) for data in recipients_data]
    return recipients


@eel.expose
def simulate(data):
    # prepare data
    satellites = prepare_satellites(data)
    objects = prepare_objects(data)
    recipients = prepare_recipient(data)

    start = int(data['start_time'])
    end = int(data['end_time'])
    step = int(data['step'])

    observation_tracker = IntersectionTracker()
    connection_tracker = IntersectionTracker()

    # simulate
    for t in range(start, end, step):
        set_progress(t, start, end, step)

        for satellite in satellites:
            for object_ in objects:
                observation_tracker.push(
                    key=(satellite.name, object_.name),
                    condition=(satellite.view_area(t).check_collision(object_)
                               and satellite.illuminated_area(t).check_collision(object_)),
                    timestamps=t
                )

        for satellite in satellites:
            for recipient in recipients:
                connection_tracker.push(
                    key=(satellite.name, recipient.name),
                    condition=(satellite.recipient_area(recipient, t).check_collision(
                        satellite.position(t).point
                    )),
                    timestamps=t
                )

    efficiency = {}
    for o_key, o_intersections in observation_tracker.intersections_store.items():
        connections = []
        for c_key, c_intersections in connection_tracker.intersections_store.items():
            if c_key[0] == o_key[0]:
                connections += c_intersections.timestamps
        connections.sort()

        efficiency[o_key] = Intersections()
        efficiency[o_key].timestamps = [
            [c_timestamps for c_timestamps in connections if c_timestamps >= o_timestamps][0]
            for o_timestamps in o_intersections.timestamps if o_timestamps <= max(connections)
        ]
        efficiency[o_key].indicators = [
            [c_timestamps - o_timestamps for c_timestamps in connections if c_timestamps >= o_timestamps][0]
            for o_timestamps in o_intersections.timestamps if o_timestamps <= max(connections)
        ]

    # add clusters
    for satellite in satellites:
        for object_ in objects:
            if satellite.cluster:
                if observation_tracker.intersections_store.get((satellite.cluster, object_.name)):
                    observation_tracker.intersections_store[(satellite.cluster, object_.name)] += \
                        observation_tracker.intersections_store[(satellite.name, object_.name)]
                else:
                    observation_tracker.intersections_store[(satellite.cluster, object_.name)] = \
                        observation_tracker.intersections_store[(satellite.name, object_.name)]

    # serialize result
    result = {
        'periodicity': {},
        'efficiency': {}
    }

    for key, intersections in observation_tracker.intersections_store.items():
        result['periodicity'][key[0]] = result['periodicity'][key[0]] \
            if result['periodicity'].get(key[0]) else {}
        result['periodicity'][key[0]][key[1]] = {
            'timestamps': intersections.timestamps,
            'indicators': intersections.indicators,
            'count': intersections.count,
            'mean_indicator': intersections.mean_indicator,
            'max_indicator': intersections.max_indicator,
            'min_indicator': intersections.min_indicator,
            'std_indicator': intersections.std_indicator,
        }

    for key, intersections in efficiency.items():
        result['efficiency'][key[0]] = result['efficiency'][key[0]] \
            if result['efficiency'].get(key[0]) else {}
        result['efficiency'][key[0]][key[1]] = {
            'timestamps': intersections.timestamps,
            'indicators': intersections.indicators,
            'count': intersections.count,
            'mean_indicator': intersections.mean_indicator,
            'max_indicator': intersections.max_indicator,
            'min_indicator': intersections.min_indicator,
            'std_indicator': intersections.std_indicator,
        }

    global last_simulation
    last_simulation = result

    set_settings('periodicity', observation_tracker.intersections_store.keys())
    set_settings('efficiency', efficiency.keys())

    return result


@eel.expose
def get_last_simulate():
    return last_simulation


@eel.expose
def map_simulation(data, t):
    satellites = prepare_satellites(data)
    objects = prepare_objects(data)
    recipients = prepare_recipient(data)

    data = []

    # observation objects
    for object_ in objects:
        data.append({
            'lon': [object_.to_deg().lambda_],
            'lat': [object_.to_deg().phi_]
        })

    # satellites
    for satellite in satellites:

        satellite_point = satellite.position(t).point.to_deg()
        data.append({
            'lon': [satellite_point.lambda_],
            'lat': [satellite_point.phi_]
        })

        satellites_view_area = satellite.view_area(t).get_border(0.1)
        data.append({
            'lon': [point.to_deg().lambda_ for point in satellites_view_area],
            'lat': [point.to_deg().phi_ for point in satellites_view_area]
        })

        satellites_illuminated_area = satellite.illuminated_area(t).get_border(0.1)
        data.append({
            'lon': [point.to_deg().lambda_ for point in satellites_illuminated_area],
            'lat': [point.to_deg().phi_ for point in satellites_illuminated_area]
        })

        for recipient in recipients:
            recipient_area = satellite.recipient_area(recipient, t).get_border(0.1)
            data.append({
                'lon': [point.to_deg().lambda_ for point in recipient_area],
                'lat': [point.to_deg().phi_ for point in recipient_area]
            })

    return data
