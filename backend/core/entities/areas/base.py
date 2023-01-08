from abc import abstractmethod
from typing import List
from backend.core.entities.point import Point
from numpy import arcsin, arccos, sin, cos, pi, arange


class SurfaceArea:
    @property
    @abstractmethod
    def alpha(self) -> float:
        """
        Центральный земной угол
        :return:
        """
        pass

    @property
    @abstractmethod
    def central_point(self) -> Point:
        """
        Центральная точка зоны
        :return:
        """
        pass

    def get_border(self, step: float = 0.1) -> List[Point]:
        """
        :param step: Шаг в радианах
        :return:
        """
        points = []
        for angle in arange(0, 2*pi, step):
            points.append(
                self.get_boundary_point(
                    phi_=self.central_point.phi_,
                    lambda_=self.central_point.lambda_,
                    alpha=self.alpha,
                    beta=angle
                )
            )

        return points

    @staticmethod
    def get_boundary_point(phi_: float,
                           lambda_: float,
                           alpha: float,
                           beta: float) -> Point:
        """
        Расчёт точки на границе зоны
        :param phi_: широта центральной точки
        :param lambda_: долгота центральной точки
        :param alpha: центральный земной угол
        :param beta: вспомогательный угол для расчета координат точек на границе
        :return: Точка на границе зоны
        """
        sin_phi = cos(alpha) * sin(phi_) - sin(alpha) * sin(beta) * cos(phi_)

        phi = arcsin(sin_phi)

        sin_lam = cos(alpha) * cos(phi_) * sin(lambda_) / cos(phi) + \
                  sin(alpha) * sin(beta) * sin(phi_) * sin(lambda_) / cos(phi) - \
                  sin(alpha) * cos(beta) * cos(lambda_) / cos(phi)

        cos_lam = cos(alpha) * cos(phi_) * cos(lambda_) / cos(phi) + \
                  sin(alpha) * sin(beta) * sin(phi_) * cos(lambda_) / cos(phi) + \
                  sin(alpha) * cos(beta) * sin(lambda_) / cos(phi)

        if sin_lam > 0 and cos_lam > 0:
            return Point(phi, arcsin(sin_lam))
        elif sin_lam > 0 and cos_lam < 0:
            return Point(phi, pi - arcsin(sin_lam))
        elif sin_lam < 0 and cos_lam < 0:
            return Point(phi, - (pi + arcsin(sin_lam)))
        elif sin_lam < 0 and cos_lam > 0:
            return Point(phi, arcsin(sin_lam))

    def check_collision(self, point: Point) -> bool:
        """
        Проверка попадания объекта наблюдения в зону
        :param point: Точка с координатами объекта
        :return:
        """
        return bool(arccos(sin(self.central_point.phi_) * sin(point.phi_) +
                           cos(self.central_point.phi_) * cos(point.phi_) *
                           cos(point.lambda_ - self.central_point.lambda_)) < self.alpha)
