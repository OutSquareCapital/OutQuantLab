from numpy.typing import NDArray
import numpy as np
from collections.abc import Callable
from typing import Any, TypeAlias

NDArrayFloat: TypeAlias = NDArray[np.float32]
ProgressFunc: TypeAlias = Callable[[int, str], Any]
IndicatorFunc : TypeAlias = Callable[[list[int]], NDArrayFloat]