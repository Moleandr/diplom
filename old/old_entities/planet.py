from dataclasses import dataclass


@dataclass
class Planet:
    # средний радиус
    R: float
    # гравитационный параметр
    Mu: float
    # угловая скорость
    omega: float
