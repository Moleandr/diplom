from core.entities import Planet, Orbit, Track
from numpy import deg2rad, rad2deg
import matplotlib.pyplot as plt


earth = Planet(
    R=6371,
    Mu=398602,
    omega=0.0000729211
)

orbit = Orbit(
    h_p=500,
    h_a=500,
    i=deg2rad(30),
    OMEGA_0=0,
    planet=earth
)

track = Track(
    t_0=1000000 * 100,
    omega_0=0,
    d_t=100,
    t_per=0,
    orbit=orbit
)

points = []
for point in track.points():
    points.append(point)
    if len(points) > 500:
        break


def print_track(points):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid()
    ax.axis([-180, 180, -90, 90])
    ax.set_yticks(list(range(-90, 90, 10)),)
    ax.set_xticks(list(range(-180, 300, 10)))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.axhline(y=0, lw=1, color='k')
    ax.axvline(x=0, lw=1, color='k')

    ax.plot([rad2deg(point.coord_lambda) for point in points], [rad2deg(point.coord_phi) for point in points])
    plt.show()

print_track(points)