from numpy import sin, cos, arctan, pi
from backend.core.entities.orbit import Orbit
from .point import Point
from ..utils.math import factorial


class OrbitPosition:
    def __init__(self,
                 orbit: Orbit,
                 t_per: float,
                 t: float):
        """
        :param orbit: Орбита
        :param t_per: Время прохождения перигея
        :param t: момент времени
        """
        self.t = t
        self.t_per = t_per
        self.orbit = orbit

    @property
    def D_t_sr(self):
        # Среднее время с момента прохождения перигея до момента наблюдения
        return self.t - self.t_per

    @property
    def t_zv(self):
        # Звёздное среднее время
        return 1.00273791 * self.D_t_sr

    @property
    def M(self):
        # Средняя аномалия
        return self.t_zv * self.orbit.n

    @property
    def E(self):
        # Эксцентрическая аномалия
        M = self.M
        e = self.orbit.e
        return M + \
               e * sin(M) + \
               e**2 / 2 * sin(2*M) + \
               e**3 / (factorial(3) * 2**2) * (3**2 * sin(3*M) - 3*sin(M)) + \
               e**4 / (factorial(4) * 2**3) * (4**3 * sin(4*M) - 4 * 2**3 * sin(2*M)) + \
               e**5 / (factorial(5) * 2**4) * (5**4 * sin(5*M) - 5 * 3**4 * sin(3*M) + 10 * sin(M)) + \
               e**6 / (factorial(6) * 2**5) * (6**5 * sin(6*M) - 6 * 4**5 * sin(4*M) + 15 * 2**2 * sin(2*M))

    @property
    def sin_Theta(self):
        # Синус истинной аномалии
        E = self.E
        e = self.orbit.e
        return sin(E)/(1 - e*cos(E)) * (1 - e**2)**(1/2)

    @property
    def cos_Theta(self):
        # Косинус истинной аномалии
        E = self.E
        e = self.orbit.e
        return (cos(E) - e)/(1 - e * cos(E))

    @property
    def Theta(self):
        # Истинная аномалия
        sin_theta = self.sin_Theta
        cos_theta = self.cos_Theta
        theta = arctan((1 - cos_theta**2)**(1/2) / cos_theta)

        if sin_theta > 0 and cos_theta < 0:
            return theta + pi
        if sin_theta < 0 and cos_theta < 0:
            return pi - theta
        if sin_theta < 0 and cos_theta > 0:
            return 2*pi - theta
        return theta

    @property
    def r(self):
        # Радиус-вектор от центра Земли в КА
        return self.orbit.p / (1 - self.orbit.e * cos(self.Theta))

    @property
    def H(self):
        # Высота полёта КА
        return self.r - self.orbit.planet.R

    @property
    def u(self):
        return self.Theta + self.orbit.omega(self.t)

    @property
    def sin_phi(self):
        # Синус широты
        return sin(self.orbit.i) * sin(self.u)

    @property
    def cos_phi(self):
        # Косинус широты
        return (1 - self.sin_phi**2)**(1/2)

    @property
    def phi_(self):
        # Широта
        return arctan(self.sin_phi/(1 - self.sin_phi**2)**(1/2))

    @property
    def sin_lambda(self):
        # Синус долготы
        OMEGA = self.orbit.OMEGA(self.t)
        u = self.u
        return (sin(OMEGA) * cos(u) + cos(OMEGA) * cos(self.orbit.i) * sin(u))/self.cos_phi

    @property
    def cos_lambda(self):
        # Косинус долготы
        OMEGA = self.orbit.OMEGA(self.t)
        u = self.u
        return (cos(OMEGA) * cos(u) - sin(OMEGA) * cos(self.orbit.i) * sin(u))/self.cos_phi

    @property
    def lambda_ga(self):
        # Долгота без возмущений
        sin_lambda = self.sin_lambda
        cos_lambda = self.cos_lambda

        if sin_lambda > 0 and cos_lambda > 0:
            return arctan(sin_lambda / (1 - sin_lambda**2)**(1/2))
        if sin_lambda > 0 and cos_lambda < 0:
            return pi + arctan((1 - cos_lambda**2)**(1/2) / cos_lambda)
        if sin_lambda < 0 and cos_lambda < 0:
            return pi - arctan(sin_lambda / (1 - sin_lambda**2)**(1/2))
        if sin_lambda < 0 and cos_lambda > 0:
            return - arctan((1 - cos_lambda**2)**(1/2) / cos_lambda)
        return 0

    @property
    def lambda_(self):
        # Долгота
        lambda_gds = self.lambda_ga - \
                   self.orbit.planet.omega * (self.t - (24 * 3600) * int(self.t/(24 * 3600))) - \
                   self.orbit.d_OMEGA * self.t / self.orbit.T_zv
        while lambda_gds > pi:
            lambda_gds = lambda_gds - 2*pi
        while lambda_gds < - pi:
            lambda_gds = lambda_gds + 2*pi

        return lambda_gds

    @property
    def point(self):
        return Point(
            self.phi_,
            self.lambda_
        )

