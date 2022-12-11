from numpy import deg2rad
from core import Spacecraft, Orbit, Point, IlluminatedArea
from core import vizualization

orbit = Orbit(
    h_p=800,
    h_a=800,
    i=deg2rad(80)
)

spacecraft = Spacecraft(
    gamma=deg2rad(60),
    orbit=orbit
)

point_on = Point(
    phi_=85,
    lambda_=110
).to_rad()

points = []
view_areas = []
illuminated_area = []

for t in range(0, 10000, 100):
    points.append(spacecraft.position(t).point)
    view_areas.append(spacecraft.view_area(t).get_border())
    illuminated_area.append(IlluminatedArea(t).get_border(step=0.01))


with vizualization.map_graph() as ax:
    ax.plot(
        [point.to_deg().lambda_ for point in points],
        [point.to_deg().phi_ for point in points]
    )

    ax.scatter(
        point_on.to_deg().lambda_,
        point_on.to_deg().phi_,
        color='blue'
    )

    for area in view_areas[:20:2]:

        ax.plot(
            [point.to_deg().lambda_ for point in area],
            [point.to_deg().phi_ for point in area]
        )

    for area in illuminated_area[::40]:

        ax.plot(
            [point.to_deg().lambda_ for point in area],
            [point.to_deg().phi_ for point in area]
        )

