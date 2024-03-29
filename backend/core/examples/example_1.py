from numpy import deg2rad, rad2deg
from backend.core import Spacecraft, Orbit, Point, IlluminatedArea

class Collisions:
    def __init__(self):
        self.values = {}

    def add(self, name: str, value: bool, **kwargs):
        if name not in self.values:
            self.values[name] = {'collisions': [], 'flag': False, 'counter': 0}
        if self.values[name]['flag'] is False and value is True:
            self.values[name]['collisions'].append(kwargs)
            self.values[name]['counter'] += 1
        self.values[name]['flag'] = value


orbit = Orbit(
    h_p=500,
    h_a=500,
    i=deg2rad(97.4)
)

spacecraft = Spacecraft(
    gamma=deg2rad(45),
    orbit=orbit
)

point_on = Point(
    phi_=60,
    lambda_=40
).to_rad()
t = 1057555
print(rad2deg(spacecraft.orbit.omega(t)))
print(rad2deg(spacecraft.position(t).Theta))
print(rad2deg(spacecraft.position(t).phi_))
print(rad2deg(spacecraft.position(t).lambda_))

-42.9729735398796
-42.975425635374

40.6430903883229
40.643090388322925

-2.31289900251157
-2.3104673635439528

-86.4153113699304
-86.41562770369347

# Ошибка вероятно не в округлении




# points = []
# view_areas = []
# illuminated_area = []
# collisions = Collisions()
#
# for t in range(0, 10000, 100):
#     points.append(spacecraft.position(t).point)
#     view_areas.append(spacecraft.view_area(t).get_border())
#     illuminated_area.append(IlluminatedArea(t).get_border(step=0.01))

# result = []
# for phi_on in range(0, 90, 5):
#     point_on = Point(
#         phi_=phi_on,
#         lambda_=40
#     ).to_rad()
#
#     for t in range(0, 1000000, 100):
#         collisions.add(
#             name='view',
#             value=spacecraft.view_area(t).check_collision(point_on) and IlluminatedArea(t).check_collision(point_on),
#             t=t
#         )
#     result.append([phi_on, 1000000/collisions.values['view']['counter']])
#
#
# print(result)
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.plot(
#     [point[0] for point in result],
#     [point[1] for point in result]
# )
# plt.show()

# points = []
# view_areas = []
# illuminated_area = []
#
# for t in range(0, 10000, 100):
#     points.append(spacecraft.position(t).point)
#     view_areas.append(spacecraft.view_area(t))
#     illuminated_area.append(IlluminatedArea(t))
#
#
# with vizualization.map_graph() as ax:
#     ax.plot(
#         [point.to_deg().lambda_ for point in points],
#         [point.to_deg().phi_ for point in points]
#     )
#
#     ax.scatter(
#         point_on.to_deg().lambda_,
#         point_on.to_deg().phi_,
#         color='green'
#     )
#
#     for area in view_areas[::5]:
#         # if area.check_collision(point_on):
#         ax.plot(
#             [point.to_deg().lambda_ for point in area.get_border()],
#             [point.to_deg().phi_ for point in area.get_border()],
#             color='blue' if area.check_collision(point_on) else "black"
#         )
#         ax.scatter(
#             area.central_point.to_deg().lambda_,
#             area.central_point.to_deg().phi_,
#             color='red'
#         )
#
#     for area in illuminated_area[::10]:
#         # if area.check_collision(point_on):
#         ax.plot(
#             [point.to_deg().lambda_ for point in area.get_border(step=0.01)],
#             [point.to_deg().phi_ for point in area.get_border(step=0.01)],
#             color='green' if area.check_collision(point_on) else "red"
#         )

