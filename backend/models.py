from typing import TypeVar, Type, Optional
from pydantic import BaseModel, validator

TData = TypeVar('TData', bound=BaseModel)


def data_factory(data, type_: Type[TData]) -> TData:
    return type_(**{field['name']: field['value'] for field in data})


class SatelliteData(BaseModel):
    name: str
    cluster: Optional[str]
    perigeeAltitude: Optional[float] = 0
    apogeeAltitude: float = 0
    orbitalInclination: float = 0
    ascendingNodeLongitude: float = 0
    initialPerigeeArgument: float = 0
    opticalRotationAngle: float = 0


class ObjectData(BaseModel):
    name: str
    latitude: float = 0
    longitude: float = 0
