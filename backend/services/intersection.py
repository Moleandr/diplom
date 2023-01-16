from dataclasses import dataclass, field
from typing import Dict, Union

import numpy as np


@dataclass
class Intersections:
    timestamps: list = field(default_factory=list)
    flag: bool = False

    @property
    def count(self):
        return len(self.timestamps)

    @property
    def indicators(self):
        return [self.timestamps[i+1] - self.timestamps[i] for i in range(len(self.timestamps) - 1)]

    @property
    def mean_indicator(self):
        if self.indicators:
            return float(np.mean(self.indicators))
        else:
            return None

    @property
    def max_indicator(self):
        if self.indicators:
            return float(np.max(self.indicators))
        else:
            return None

    @property
    def min_indicator(self):
        if self.indicators:
            return float(np.min(self.indicators))
        else:
            return None

    @property
    def std_indicator(self):
        if self.indicators:
            return float(np.std(self.indicators))
        else:
            return None

    def __add__(self, otherIntersections: "Intersections"):
        sum_intersection = Intersections()
        sum_intersection.timestamps = self.timestamps + otherIntersections.timestamps
        return sum_intersection


class IntersectionTracker:
    def __init__(self):
        self.intersections_store: Dict[Union[str, tuple], Intersections] = {}

    def __repr__(self):
        return f'IntersectionTracker({list(self.intersections_store.keys())})'

    def push(self, key: Union[str, tuple], condition: bool, timestamps: float = 0):
        if key not in self.intersections_store:
            self.intersections_store[key] = Intersections()

        if self.intersections_store[key].flag is False and condition is True:
            self.intersections_store[key].timestamps.append(timestamps)

        self.intersections_store[key].flag = condition
