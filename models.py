from dataclasses import dataclass


@dataclass
class Point:
    coord_phi: float
    coord_lambda: float


@dataclass
class SpaceCraft(Point):
    gamma: float
    hight: float