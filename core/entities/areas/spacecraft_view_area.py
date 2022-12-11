from ..point import Point
from core.entities.areas.base import SurfaceArea
from numpy import arcsin, arccos, tan


class SpacecraftViewArea(SurfaceArea):
    def __init__(self,
                 phi_: float,
                 lambda_: float,
                 R: float,
                 H: float,
                 gamma: float):
        """
        :param phi_: Широта подспутниковой точки
        :param lambda_: Долгота подспутниковой точки
        :param R: Радиус Орбиты
        :param H: Высота КА
        :param gamma: Угол поворота оптической оси КА
        """
        self.phi_ = phi_
        self.lambda_ = lambda_
        self.R = R
        self.H = H
        self.gamma = gamma

    @property
    def central_point(self) -> Point:
        return Point(phi_=self.phi_, lambda_=self.lambda_)

    @property
    def alpha(self) -> float:
        # Центральный земной угол
        return arcsin((self.H + self.R) / self.R * tan(self.gamma) /
                      (1 + tan(self.gamma) ** 2) ** (1 / 2)) - \
               arccos(1 / (1 + tan(self.gamma) ** 2) ** (1 / 2))


