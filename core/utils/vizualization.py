from contextlib import contextmanager
import matplotlib.pyplot as plt


@contextmanager
def map_graph():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid()
    ax.axis([-180, 180, -90, 90])
    ax.set_yticks(list(range(-90, 90, 10)))
    ax.set_xticks(list(range(-180, 180, 10)))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.axhline(y=0, lw=1, color='k')
    ax.axvline(x=0, lw=1, color='k')

    yield ax

    plt.show()
