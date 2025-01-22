from typing import Final
from outquantlab.typing_conventions.custom_types import Float32

ANNUALIZATION_FACTOR: Final = Float32(16)
PERCENTAGE_FACTOR: Final = Float32(100)
ANNUALIZED_PERCENTAGE_FACTOR: Final = Float32(ANNUALIZATION_FACTOR * PERCENTAGE_FACTOR)