import numpy
from functools import lru_cache


@lru_cache
def factorial(number: int):
    return numpy.math.factorial(number)
