from numpy.typing import NDArray
from numpy import float32, int32
from collections.abc import Callable
from typing import TypeAlias

Float32: TypeAlias = float32
Int32: TypeAlias = int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]
ProgressFunc: TypeAlias = Callable[[int, str], None]
ClustersHierarchy: TypeAlias = dict[str, dict[str, list[str]]]