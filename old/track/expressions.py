from numpy import pi
from numpy import sin, cos, tan
from numpy import arcsin, arccos
from numpy import deg2rad, rad2deg


# CONSTANTS

# Earth params
R_z = 6371
Mu_z = 398602
Omega_z = 0.0000729211

# Orbit params
i = 1
Omega_0 = 1
omega_0 = 1
H_p = 1
H_a = 1
t_0 = 1
t_pereg = 1


def get_orbit_radius(Rz: float, H: float):
    return Rz + H


def get_e(r_p: float, r_a: float):
    return (r_a - r_p)/(r_a + r_p)


def get_a(r_p, r_a):
    return (r_p + r_a)/2


def get_T_zv(a, Mu_z):
    return 2*pi * (a**3/Mu_z)**(1/2)


def get_p(a, e):
    return a * (1 - e**2)


def get_delta_Omega(R_z, p, i):
    return -35.052/60 * (R_z/p)**2 * cos(i)


def get_Omega(delta_Omega, t, t_zv, Omega_0):
    return Omega_0 + t/t_zv * delta_Omega


def get_delta_omega(R_z, p, i):
    return -17.525/60 * (R_z/p)**2 * (1 - 5*(cos(i))**2)


def get_omega(delta_omega, omega_0, t, t_zv):
    return omega_0 + t/t_zv * delta_omega


def get_n(Mu_z, a):
    return (Mu_z/a**3)**(1/2)

def get_delta_t_sr(t, t_pereg):
    return t - t_pereg

def get_t_zv(delta_t_sr):
    return 1.00273791 * delta_t_sr

def get_M(t_zv, n):
    return t_zv * n



# E01 := Msr + e * sin(Msr) + (e * e / 2) * sin(2 * Msr); // Первый член разложения уравнения // Кеплера(E - e * sin(E) = M
# E02 := e * e * e / 24 * (9 * sin(3 * Msr) - 3 * sin(Msr)); // Второй членразложения и т.д.
# E03 := e * e * e * e / (24 * 8) * (64 * sin(4 * Msr) - 32 * sin(2 * Msr));
# E04 := e * e * e * e * e / (120 * 16) * (625 * sin(5 * Msr) + 5 * 81 * sin(3 * Msr) + 10 * sin(Msr));
# E05 := e * e * e * e * e * e / (720 * 32) * (36 * 36 * 6 * sin(6 * Msr)


if __name__ == '__main__':
    # Расчёт
    r_p = get_orbit_radius(R_z, H_p)
    r_a = get_orbit_radius(R_z, H_a)
    e = get_e(r_p, r_a)
    a = get_a(r_p, r_a)
    T_zv = get_T_zv(a, Mu_z)
    p = get_p(a, e)
    delta_Omega = get_delta_Omega(R_z, p, i)
    Omega = get_Omega(delta_Omega, t_0, T_zv, Omega_0)
    delta_omega = get_delta_omega(R_z, p, i)
    omega = get_omega(delta_omega, omega_0, t_0, T_zv)
    n = get_n(Mu_z, a)
    delta_t_sr = get_delta_t_sr(t_0, t_pereg)
    t_zv = get_t_zv(delta_t_sr)
    M = get_M(t_zv, n)








