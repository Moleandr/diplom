from .orbit import Orbit
from .position import OrbitPosition
from .areas.spacecraft_view_area import SpacecraftViewArea
from .areas.illuminated_area import IlluminatedArea
from .areas.recipient_area import RecipientArea


class Spacecraft:
    def __init__(self,
                 gamma: float,
                 orbit: Orbit,
                 t_per: float = 0,
                 y_s: float = 0):
        """
        :param gamma: Угол поворота относительно надира
        :param orbit: Орбита КА
        :param t_per: Время прохождения перигея
        :param y_s: минимальная высота Солнца над горизонтом, град
        """
        self.gamma = gamma
        self.orbit = orbit
        self.t_per = t_per
        self.y_s = y_s

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

    def illuminated_area(self, t) -> IlluminatedArea:
        return IlluminatedArea(
            t=t,
            y_s=self.y_s
        )

    def recipient_area(self, point, t) -> RecipientArea:
        return RecipientArea(
            phi_=point.phi_,
            lambda_=point.lambda_,
            R=self.orbit.planet.R,
            H=self.position(t).H,
        )
