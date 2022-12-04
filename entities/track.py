from collections.abc import Iterable
from numpy import sin, cos, arctan, pi

from .orbit import Orbit
from .point import Point
from entities.math import factorial


class Track:
    def __init__(self,
                 t_0: float,
                 omega_0: float,
                 d_t: float,
                 t_per: float,
                 orbit: Orbit):
        """
        :param t_0: Начальное время
        :param omega_0: Начальный аргумент перигея
        :param d_t: Шаг расчёта по времени
        :param t_per: Время первого прохождения перигея
        :param orbit: Орбита
        """
        self.t_0 = t_0
        self.omega_0 = omega_0
        self.d_t = d_t
        self.t_per = t_per
        self.orbit = orbit

    def points(self) -> Iterable[Point]:
        t_current = self.t_0
        while True:
            yield Point(self.phi_gd(t_current), self.lambda_gd(t_current))
            t_current += self.d_t

    def OMEGA(self, t):
        return self.orbit.OMEGA_0 + t / self.orbit.T_zv * self.orbit.d_OMEGA

    def omega(self, t):
        return self.omega_0 + t / self.orbit.T_zv * self.orbit.d_omega

    def D_t_sr(self, t):
        return t - self.t_per

    def t_zv(self, t):
        return 1.00273791 * self.D_t_sr(t)

    def M(self, t):
        return self.t_zv(t) * self.orbit.n

    def E(self, t):
        M = self.M(t)
        e = self.orbit.e
        return M + \
               e * sin(M) + \
               e**2 / 2 * sin(2*M) + \
               e**3 / (factorial(3) * 2**2) * (3**2 * sin(3*M) - 3*sin(M)) + \
               e**4 / (factorial(4) * 2**3) * (4**3 * sin(4*M) - 4 * 2**3 * sin(2*M)) + \
               e**5 / (factorial(5) * 2**4) * (5**4 * sin(5*M) - 5 * 3**4 * sin(3*M) + 10 * sin(M)) + \
               e**6 / (factorial(6) * 2**5) * (6**5 * sin(6*M) - 6 * 4**5 * sin(4*M) + 15 * 2**2 * sin(2*M))

    def sin_Theta(self, t):
        E = self.E(t)
        e = self.orbit.e
        return sin(E)/(1 - e*cos(E)) * (1 - e**2)**(1/2)

    def cos_Theta(self, t):
        E = self.E(t)
        e = self.orbit.e
        return (cos(E) - e)/(1 - e * cos(E))

    def Theta(self, t):
        # TODO Перепроверить взято из исходного кода EFKAN
        sin_teta = self.sin_Theta(t)
        cos_teta = self.cos_Theta(t)
        theta = arctan((1 - cos_teta**2)**(1/2) / cos_teta)

        if sin_teta > 0 and cos_teta < 0:
            return theta + pi
        if sin_teta < 0 and cos_teta < 0:
            return pi - theta
        if sin_teta < 0 and cos_teta > 0:
            return 2 * pi - theta
        return theta

    def u(self, t):
        return self.Theta(t) + self.omega(t)

    def sin_phi(self, t):
        return sin(self.orbit.i) * sin(self.u(t))

    def cos_phi(self, t):
        return (1 - self.sin_phi(t)**2)**(1/2)

    def phi_ga(self, t):
        return arctan(self.sin_phi(t)/(1 - self.sin_phi(t)**2)**(1/2))

    def sin_lambda(self, t):
        OMEGA = self.OMEGA(t)
        u = self.u(t)
        return (sin(OMEGA) * cos(u) + cos(OMEGA) * cos(self.orbit.i) * sin(u))/self.cos_phi(t)

    def cos_lambda(self, t):
        OMEGA = self.OMEGA(t)
        u = self.u(t)
        return (cos(OMEGA) * cos(u) - sin(OMEGA) * cos(self.orbit.i) * sin(u))/self.cos_phi(t)

    # Что здесь происходит?
    def lambda_ga(self, t):
        sin_lambda = self.sin_lambda(t)
        cos_lambda = self.cos_lambda(t)

        if sin_lambda > 0 and cos_lambda > 0:
            return arctan(sin_lambda / (1 - sin_lambda**2)**(1/2))
        if sin_lambda > 0 and cos_lambda < 0:
            return pi + arctan((1 - cos_lambda**2)**(1/2) / cos_lambda)
        if sin_lambda < 0 and cos_lambda < 0:
            return pi - arctan(sin_lambda / (1 - sin_lambda**2)**(1/2))
        if sin_lambda < 0 and cos_lambda > 0:
            return - arctan((1 - cos_lambda**2)**(1/2) / cos_lambda)
        return 0

    def phi_gd(self, t):
        return self.phi_ga(t)

    # Зачем округление времени?
    def lambda_gd(self, t):
        lambda_gds = self.lambda_ga(t) - \
                   self.orbit.planet.omega * (t - (24 * 3600) * int(t/(24 * 3600))) - \
                   self.orbit.d_OMEGA * t / self.orbit.T_zv
        while lambda_gds > pi:
            lambda_gds = lambda_gds - 2*pi
        while lambda_gds < - pi:
            lambda_gds = lambda_gds + 2*pi

        return lambda_gds