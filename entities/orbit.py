from functools import cached_property
from numpy import pi, cos, deg2rad

from .planet import Planet


class Orbit:
    def __init__(self,
                 h_p: float,
                 h_a: float,
                 i: float,
                 OMEGA_0: float,
                 planet: Planet):
        """
        :param h_p: Высота перигея
        :param h_a: Высота апогея
        :param i: Угол наклона орбиты
        :param OMEGA_0: Долгота восходящего узла
        :param planet: Планета орбиты
        """
        self.h_p = h_p
        self.h_a = h_a
        self.i = i
        self.OMEGA_0 = OMEGA_0
        self.planet = planet

    @cached_property
    def r_a(self):
        # Радиус апогея
        return self.planet.R + self.h_a

    @cached_property
    def r_p(self):
        # Радиус перигея
        return self.planet.R + self.h_p

    @cached_property
    def e(self):
        # Эксцентриситет
        return (self.r_a - self.r_p)/(self.r_a + self.r_p)

    @cached_property
    def a(self):
        # Большая полуось
        return (self.r_p + self.r_a)/2

    @cached_property
    def p(self):
        # Фокальный параметр
        return self.a * (1 - self.e**2)

    @cached_property
    def T_zv(self):
        # Величина звёздного периода обращения
        return 2 * pi * (self.a**3 / self.planet.Mu)**(1/2)

    @cached_property
    def d_OMEGA(self):
        # Вековое возмущение первого порядка долготы восходящего узла
        return deg2rad(-35.052/60) * (self.planet.R/self.p)**2 * cos(self.i)

    @cached_property
    def d_omega(self):
        # Вековое возмущение первого порядка аргумент перигея
        return deg2rad(-17.525/60) * (self.planet.R/self.p)**2 * \
               (1 - 5*(cos(self.i))**2)

    @cached_property
    def n(self):
        # Среднее движение
        return (self.planet.Mu / self.a**3)**(1/2)
