from numpy.typing import NDArray
from numpy import float32, int32
from typing import TypeAlias
from collections.abc import Callable

Float32: TypeAlias = float32
Int32: TypeAlias = int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]
RollingStatFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
OverallStatFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]