from typing import List
from .orbit import Orbit
from .point import Point
from .position import OrbitPosition
from .areas.spacecraft_view_area import SpacecraftViewArea


class Spacecraft:
    def __init__(self,
                 gamma: float,
                 orbit: Orbit,
                 t_per: float = 0):
        """
        :param gamma: Угол поворота относительно надира
        :param orbit: Орбита КА
        :param t_per: Время прохождения перигея
        """
        self.gamma = gamma
        self.orbit = orbit
        self.t_per = t_per

    def position(self, t) -> OrbitPosition:
        return OrbitPosition(
            orbit=self.orbit,
            t_per=self.t_per,
            t=t
        )

    def view_area(self, t) -> SpacecraftViewArea:
        return SpacecraftViewArea(
            phi_=self.position(t).phi_,
            lambda_=self.position(t).lambda_,
            R=self.orbit.planet.R,
            H=self.position(t).H,
            gamma=self.gamma
        )
