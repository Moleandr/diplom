from .point import Point
from numpy import arcsin, arccos, tan, sin, cos, pi, deg2rad, arange


class ViewArea:
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
    def alpha(self) -> float:
        # Центральный земной угол
        return arcsin((self.H + self.R) / self.R * tan(self.gamma) /
                      (1 + tan(self.gamma) ** 2) ** (1 / 2)) - \
               arccos(1 / (1 + tan(self.gamma) ** 2) ** (1 / 2))

    def check_collision(self, point: Point) -> bool:
        """
        Проверка попадания объекта наблюдения в зону обзора аппаратуры зондирования КА
        :param point: Точка с координатами наблюдаемого объекта
        :return:
        """
        return arccos(sin(self.phi_) * sin(point.phi_) +
                      cos(self.phi_) * cos(point.phi_) *
                      cos(point.lambda_ - self.lambda_)) < self.alpha

    def boarder_points(self, step: float = 0.1):
        # Граничные точки
        points = []
        for angle in arange(0, 2*pi, step):
            phi_, lambda_ = self.view_area_boundary_point(
                phi_ka=self.phi_,
                lambda_ka=self.lambda_,
                alpha=self.alpha,
                beta=angle
            )

            points.append(Point(phi_, lambda_))

        return points

    @staticmethod
    def view_area_boundary_point(phi_ka: float,
                                 lambda_ka: float,
                                 alpha: float,
                                 beta: float):
        """
        Расчёт точки на границе зоны обзора КА
        :param phi_ka: широта подспутниковой точки КА (радианы)
        :param lambda_ka: долгота подспутниковой точки КА (радианы)
        :param alpha: центральный земной угол зоны наблюдения КА (радианы)
        :param beta: вспомогательный угол для расчета координат точек на границе зоны обзора КА
        :return: Координаты широты и долготы точки на границе зоны обзора
        """
        sin_phi = cos(alpha) * sin(phi_ka) - sin(alpha) * sin(beta) * cos(phi_ka)

        phi = arcsin(sin_phi)

        sin_lam = cos(alpha) * cos(phi_ka) * sin(lambda_ka) / cos(phi) + \
                  sin(alpha) * sin(beta) * sin(phi_ka) * sin(lambda_ka) / cos(phi) - \
                  sin(alpha) * cos(beta) * cos(lambda_ka) / cos(phi)

        cos_lam = cos(alpha) * cos(phi_ka) * cos(lambda_ka) / cos(phi) + \
                  sin(alpha) * sin(beta) * sin(phi_ka) * cos(lambda_ka) / cos(phi) + \
                  sin(alpha) * cos(beta) * sin(lambda_ka) / cos(phi)

        if sin_lam > 0 and cos_lam > 0:
            return phi, arcsin(sin_lam)
        elif sin_lam > 0 and cos_lam < 0:
            return phi, pi - arcsin(sin_lam)
        elif sin_lam < 0 and cos_lam < 0:
            return phi, - (pi + arcsin(sin_lam))
        elif sin_lam < 0 and cos_lam > 0:
            return phi, arcsin(sin_lam)


