from dataclasses import dataclass


@dataclass
class Planet:
    R: float  # средний радиус
    Mu: float  # гравитационный параметр
    omega: float  # угловая скорость
