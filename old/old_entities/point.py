from dataclasses import dataclass


@dataclass
class Point:
    # Широта
    phi_: float
    # Долгота
    lambda_: float
