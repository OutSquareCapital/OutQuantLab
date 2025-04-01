from outquantlab.structures import Float32
from enum import Enum

class Standardization(Enum):
    ANNUALIZATION = Float32(16)
    PERCENTAGE = Float32(100)
    ANNUALIZED_PERCENTAGE = Float32(ANNUALIZATION * PERCENTAGE)

class TimePeriod(Enum):
    WEEK = 5
    MONTH = 21
    QUARTER = 63
    HALF_YEAR = 126
    YEAR = 252
    HALF_DECADE = 1260
    DECADE = 2520