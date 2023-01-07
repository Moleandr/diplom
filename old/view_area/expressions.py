from numpy import pi
from numpy import sin, cos, tan
from numpy import arcsin, arccos
from numpy import deg2rad, rad2deg

# expressions
def get_alpha(H: float, Rz: float, gamma: float):
    """
    Расчёт центрального земного угла зоны наблюдения КА
    :param H: Высота орбиты(км)
    :param Rz: Радиус Земли(км)
    :param gamma: Угол поворота оптической оси КА(радианы)
    :return:  центральный земной угол зоны наблюдения(радианы)
    """
    return \
        arcsin((H + Rz) / Rz * tan(gamma) / (1 + tan(gamma) ** 2) ** (1 / 2)) - \
        arccos(1 / (1 + tan(gamma) ** 2) ** (1 / 2))

def check_collision(phi_ka: float,
                    lambda_ka: float,
                    phi_on: float,
                    lambda_on: float,
                    alpha: float) -> bool:
    """
    Проверка попадания объекта наблюдения в зону обзора аппаратуры зондирования КА
    :param phi_ka: широта подспутниковой точки КА (радианы)
    :param lambda_ka: долгота подспутниковой точки КА (радианы)
    :param phi_on: широта объекта наблюдения (радианы)
    :param lambda_on: долгота объекта наблюдения (радианы)
    :param alpha: центральный земной угол зоны наблюдения КА (радианы)
    :return:
    """
    return arccos(
        sin(phi_ka)*sin(phi_on) + cos(phi_ka)*cos(phi_on)*cos(lambda_on-lambda_ka)
    ) < alpha


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
    sin_phi = cos(alpha)*sin(phi_ka) - sin(alpha)*sin(beta)*cos(phi_ka)

    phi = arcsin(sin_phi)

    sin_lam = cos(alpha)*cos(phi_ka)*sin(lambda_ka)/cos(phi) + \
              sin(alpha)*sin(beta)*sin(phi_ka)*sin(lambda_ka)/cos(phi) - \
              sin(alpha)*cos(beta)*cos(lambda_ka)/cos(phi)

    cos_lam = cos(alpha)*cos(phi_ka)*cos(lambda_ka)/cos(phi) + \
              sin(alpha)*sin(beta)*sin(phi_ka)*cos(lambda_ka)/cos(phi) + \
              sin(alpha)*cos(beta)*sin(lambda_ka)/cos(phi)

    if sin_lam > 0 and cos_lam > 0:
        return phi, arcsin(sin_lam)
    elif sin_lam > 0 and cos_lam < 0:
        return phi, pi - arcsin(sin_lam)
    elif sin_lam < 0 and cos_lam < 0:
        return phi, - (pi + arcsin(sin_lam))
    elif sin_lam < 0 and cos_lam > 0:
        return phi, arcsin(sin_lam)


import warnings
import matplotlib
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)


def collision_vizualization(spacecraft: SpaceCraft,
                            obs_object: Point,
                            Rz: float = 6371):
    alpha = get_alpha(spacecraft.hight, Rz, spacecraft.gamma)

    mass_phi = []
    mass_lambda = []
    for angle in range(0, 360):
        phi, lambda_ = view_area_boundary_point(
            phi_ka=spacecraft.coord_phi,
            lambda_ka=spacecraft.coord_lambda,
            alpha=alpha,
            beta=deg2rad(angle)
        )
        mass_phi.append(rad2deg(phi))
        mass_lambda.append(rad2deg(lambda_))

    # graph options
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid()
    ax.axis([-180, 180, -90, 90])
    ax.set_yticks(list(range(-90, 90, 10)),)
    ax.set_xticks(list(range(-180, 180, 10)))
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    ax.axhline(y=0, lw=1, color='k')
    ax.axvline(x=0, lw=1, color='k')

    ax.plot(mass_lambda, mass_phi)

    if check_collision(
        phi_ka=spacecraft.coord_phi,
        lambda_ka=spacecraft.coord_lambda,
        phi_on=obs_object.coord_phi,
        lambda_on=obs_object.coord_lambda,
        alpha=alpha
    ):
        ax.scatter(
            rad2deg(obs_object.coord_lambda),
            rad2deg(obs_object.coord_phi),
            color='green'
        )
    else:
        ax.scatter(
            rad2deg(obs_object.coord_lambda),
            rad2deg(obs_object.coord_phi),
            color='red'
        )

    plt.show()


spacecraft = SpaceCraft(
    coord_phi=deg2rad(-60),
    coord_lambda=deg2rad(180),
    gamma=deg2rad(60),
    hight=700
)

obs_object = Point(
    coord_phi=deg2rad(40),
    coord_lambda=deg2rad(68),
)

collision_vizualization(spacecraft, obs_object)


