from outquantlab.structures import arrays
from enum import IntEnum

ZERO = arrays.Float32(0.0)
ONE = arrays.Float32(1.0)
ANNUALIZATION = arrays.Float32(16)
PERCENTAGE = arrays.Float32(100)
ANNUALIZED_PERCENTAGE = arrays.Float32(ANNUALIZATION * PERCENTAGE)

class TimePeriod(IntEnum):
    WEEK = 5
    MONTH = 21
    QUARTER = 63
    HALF_YEAR = 126
    YEAR = 252
    HALF_DECADE = 1260
    DECADE = 2520