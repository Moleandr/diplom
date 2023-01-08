from dataclasses import dataclass, field
from typing import Dict, Union


@dataclass
class Intersections:
    timestamps: list = field(default_factory=list)
    flag: bool = False

    @property
    def count(self):
        return len(self.timestamps)


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
