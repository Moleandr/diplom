from ..point import Point
from backend.core.entities.areas.base import SurfaceArea
from numpy import arccos


class RecipientArea(SurfaceArea):
    def __init__(self,
                 phi_: float,
                 lambda_: float,
                 R: float,
                 H: float):
        """
        :param phi_: Широта подспутниковой точки
        :param lambda_: Долгота подспутниковой точки
        :param R: Радиус планеты
        :param H: Высота КА
        """
        self.phi_ = phi_
        self.lambda_ = lambda_
        self.R = R
        self.H = H

    @property
    def central_point(self) -> Point:
        return Point(phi_=self.phi_, lambda_=self.lambda_)

    @property
    def alpha(self) -> float:
        # Центральный земной угол
        return arccos(self.R / (self.R + self.H))


