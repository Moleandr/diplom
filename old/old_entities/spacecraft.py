from .point import Point
from .orbit import Orbit

class SpaceCraft:
    def __init__(self,
                 coords: Point,
                 orbit: Orbit):
        self.coords = coords
        self.orbit = orbit