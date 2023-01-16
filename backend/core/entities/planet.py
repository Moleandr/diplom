from dataclasses import dataclass


@dataclass
class Planet:
    R: float = 6371  # средний радиус
    Mu: float = 398700  # гравитационный параметр
    omega: float = 0.0000729211  # угловая скорость
