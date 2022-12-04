from numpy import rad2deg, deg2rad


class Point:
    def __init__(self,
                 phi_: float,
                 lambda_: float):
        self.phi_ = phi_
        self.lambda_ = lambda_

    def __repr__(self):
        return f"Point(phi={self.phi_}, lambda={self.lambda_})"

    def convert_to_deg(self) -> "Point":
        return Point(
            rad2deg(self.phi_),
            rad2deg(self.lambda_)
        )

    def convert_to_rad(self) -> "Point":
        return Point(
            deg2rad(self.phi_),
            deg2rad(self.lambda_)
        )

