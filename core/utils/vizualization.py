from contextlib import contextmanager
import matplotlib.pyplot as plt


@contextmanager
def map_graph(x_min: int = -180,
              x_max: int = 180,
              y_min: int = -90,
              y_max: int = 90):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid()
    ax.axis([x_min, x_max, y_min, y_max])
    ax.set_yticks(list(range(-90, 90, 10)))
    ax.set_xticks(list(range(-180, 180, 10)))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.axhline(y=0, lw=1, color='k')
    ax.axvline(x=0, lw=1, color='k')

    yield ax

    plt.show()

@contextmanager
def map_graph(x_min: int = -180,
              x_max: int = 180,
              y_min: int = -90,
              y_max: int = 90):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid()
    ax.axis([x_min, x_max, y_min, y_max])
    ax.set_yticks(list(range(-90, 90, 10)))
    ax.set_xticks(list(range(-180, 180, 10)))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.axhline(y=0, lw=1, color='k')
    ax.axvline(x=0, lw=1, color='k')

    yield ax

    plt.show()
