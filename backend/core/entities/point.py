from typing import TypeVar
from copy import deepcopy
from numpy import rad2deg, deg2rad

TPoint = TypeVar('TPoint', bound="Point")


class Point:
    def __init__(self,
                 phi_: float,
                 lambda_: float):
        self.phi_ = phi_
        self.lambda_ = lambda_

    def __repr__(self):
        return f"Point(phi={self.phi_}, lambda={self.lambda_})"

    def to_deg(self: TPoint) -> TPoint:
        obj = deepcopy(self)
        obj.phi_ = rad2deg(self.phi_)
        obj.lambda_ = rad2deg(self.lambda_)
        return obj

    def to_rad(self) -> "Point":
        obj = deepcopy(self)
        obj.phi_ = deg2rad(self.phi_)
        obj.lambda_ = deg2rad(self.lambda_)
        return obj

