from typing import List

import eel
from numpy import deg2rad

from .models import data_factory
from .models import SatelliteData, ObjectData
from .services.intersection import IntersectionTracker
from .core import Spacecraft, Orbit, Point, IlluminatedArea


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
        orbit=orbit
    )
    return spacecraft


def object_factory(data: ObjectData) -> ObservationObject:
    return ObservationObject(
        name=data.name,
        phi_=data.latitude,
        lambda_=data.longitude
    ).to_rad()


def set_progress(time, start_time, end_time, step):
    percent = (end_time - start_time) / 100
    progress = time // percent
    if time % percent < step:
        eel.setProgress(progress + 1)


def set_settings(settings):
    eel.setPeriodicitySettings([{'name': f'{el[0]}|{el[1]}'} for el in settings])


def prepare_satellites(data) -> List[Satellite]:
    satellites_data = [data_factory(el, SatelliteData) for el in data['satellites']]
    satellites = [satellite_factory(data) for data in satellites_data]
    return satellites


def prepare_objects(data) -> List[ObservationObject]:
    objects_data = [data_factory(el, ObjectData) for el in data['objects']]
    objects = [object_factory(data) for data in objects_data]
    return objects


@eel.expose
def simulate(data):
    # prepare data
    satellites = prepare_satellites(data)
    objects = prepare_objects(data)

    start = int(data['start_time'])
    end = int(data['end_time'])
    step = int(data['step'])

    tracker = IntersectionTracker()

    # simulate
    for t in range(start, end, step):
        set_progress(t, start, end, step)

        for satellite in satellites:
            for object_ in objects:
                tracker.push(
                    key=(satellite.name, object_.name),
                    condition=(satellite.view_area(t).check_collision(object_)
                               and IlluminatedArea(t).check_collision(object_)),
                    timestamps=t
                )

    # serialize result
    result = {}
    for key, intersections in tracker.intersections_store.items():
        result[key[0]] = result[key[0]] if result.get(key[0]) else {}
        result[key[0]][key[1]] = {
            'timestamps': intersections.timestamps,
            'periodicity_indicator': (end-start) / intersections.count
        }

    global last_simulation
    last_simulation = result

    set_settings(tracker.intersections_store.keys())

    return result


@eel.expose
def get_last_simulate():
    return last_simulation


@eel.expose
def map_simulation(data, t):
    satellites = prepare_satellites(data)
    objects = prepare_objects(data)

    satellites_points = [satellite.position(t).point.to_deg() for satellite in satellites]
    satellites_areas = [satellite.view_area(t).get_border(0.1) for satellite in satellites]
    illuminated_area = IlluminatedArea(t).get_border(0.1)

    data = []
    data += [{'lon': [el.to_deg().lambda_], 'lat': [el.to_deg().phi_]} for el in objects]
    data += [{'lon': [point.lambda_], 'lat': [point.phi_]} for point in satellites_points]
    data += [{
        'lon': [point.to_deg().lambda_ for point in area],
        'lat': [point.to_deg().phi_ for point in area]
    } for area in satellites_areas]
    data += [{
        'lon': [point.to_deg().lambda_ for point in illuminated_area],
        'lat': [point.to_deg().phi_ for point in illuminated_area]
    }]
    return data
