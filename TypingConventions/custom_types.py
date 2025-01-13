from numpy.typing import NDArray
from numpy import float32, int32
from collections.abc import Callable
from typing import TypeAlias
from plotly.graph_objects import Figure # type: ignore

Float32: TypeAlias = float32
Int32: TypeAlias = int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]
ProgressFunc: TypeAlias = Callable[[int, str], None]
IndicatorFunc : TypeAlias = Callable[..., ArrayFloat]
ClustersHierarchy: TypeAlias = dict[str, dict[str, list[str]]]
GraphFunc: TypeAlias =  Callable[..., str|Figure]