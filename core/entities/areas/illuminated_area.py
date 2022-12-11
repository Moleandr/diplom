from ..point import Point

from core.entities.areas.base import SurfaceArea
from numpy import arcsin, sin, cos, pi, deg2rad, arctan, clip


class IlluminatedArea(SurfaceArea):
    def __init__(self,
                 t: float,
                 omega: float = 0.0000729211):
        """
        :param t: Время от начала расчёта
        :param omega: Угловая скорость вращения планеты
        (При котором угол весеннего равноденствия совпадает с направлением на Солнце)
        Прим. Для Земли
        """
        self.t = t
        self.omega = omega

    @property
    def a_c(self) -> float:
        """
        Угол между направлением на точку весеннего равноденствия и направлением на Солнце
        :return:
        """
        return (2*pi*self.t) / (365.2422 * 24 * 3600)

    @property
    def d_c(self) -> float:
        """
        Угол между эклиптикой и экватором, рад
        :return:
        """
        return deg2rad(23.343)

    @property
    def central_point(self) -> Point:
        """
        # Расчёт точки, в которой Солнце находится в зените
        :return:
        """
        # Проекция вектора на Солнце
        s_x = cos(self.a_c)
        s_y = sin(self.a_c) * cos(self.d_c)
        s_z = sin(self.a_c) * sin(self.d_c)

        # Расчёт широты
        phi_ = arctan(s_z)

        # Расчёт долготы
        sin_lambda_ = clip(s_y / cos(phi_), -1, 1)
        cos_lambda_ = clip(s_x / cos(phi_), -1, 1)

        if sin_lambda_ > 0 and cos_lambda_ > 0:
            lambda_ = arcsin(sin_lambda_)
        elif sin_lambda_ > 0 and cos_lambda_ < 0:
            lambda_ = pi - arcsin(sin_lambda_)
        elif sin_lambda_ < 0 and cos_lambda_ < 0:
            lambda_ = - pi - arcsin(sin_lambda_)
        else:
            lambda_ = arcsin(sin_lambda_)

        # Учёт скорости вращения планеты
        lambda_ = lambda_ - self.omega * (self.t - (24*3600) * int(self.t / (24*3600)))

        return Point(phi_=phi_, lambda_=lambda_)

    @property
    def alpha(self) -> float:
        return pi / 2
