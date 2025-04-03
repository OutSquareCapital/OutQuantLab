from typing import TypeAlias

from numpy import float32, int32, nan
from numpy.typing import NDArray

Nan: float = nan
Float32: TypeAlias = float32
Int32: TypeAlias = int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]