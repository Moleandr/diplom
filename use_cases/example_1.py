from numpy import deg2rad
from core import Spacecraft, Orbit, Planet, Point
from core import vizualization


earth = Planet(
    R=6371,
    Mu=398602,
    omega=0.0000729211
)

orbit = Orbit(
    h_p=800,
    h_a=800,
    i=deg2rad(60),
    OMEGA_0=deg2rad(0),
    omega_0=deg2rad(0),
    planet=earth
)

spacecraft = Spacecraft(
    gamma=deg2rad(60),
    orbit=orbit,
    t_per=0
)

point_on = Point(
    phi_=60,
    lambda_=90
).convert_to_rad()

points = []
view_areas = []
for t in range(0, 100000, 100):
    points.append(spacecraft.position(t).point)
    view_areas.append(spacecraft.view_area(t))

with vizualization.map_graph() as ax:
    ax.plot(
        [point.convert_to_deg().lambda_ for point in points],
        [point.convert_to_deg().phi_ for point in points]
    )

    ax.scatter(
        point_on.convert_to_deg().lambda_,
        point_on.convert_to_deg().phi_,
        color='blue'
    )

    for area in view_areas[:40:2]:
        ax.plot(
            [point.convert_to_deg().lambda_ for point in area.boarder_points()],
            [point.convert_to_deg().phi_ for point in area.boarder_points()],
            color='green' if area.check_collision(point_on) else 'red'
        )

# with vizualization.map_graph() as ax:
#     points = spacecraft.view_area(0).boarder_points()
#     print(spacecraft.position(0).lambda_)
#     print(spacecraft.position(0).phi_)
#     print(spacecraft.position(0).H)
#     print(spacecraft.view_area(0).alpha)
#
#     print(points[2].convert_to_deg())
#
#     ax.plot(
#         [point.convert_to_deg().lambda_ for point in points],
#         [point.convert_to_deg().phi_ for point in points]
#     )

