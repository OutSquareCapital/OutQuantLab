from numpy.typing import NDArray
import numpy as np
import pandas as pd
from collections.abc import Callable
from typing import Any

NDArrayFloat = NDArray[np.float32]
ProgressFunc = Callable[[int, str], Any]
IndicatorFunc = Callable[[list[int]], NDArrayFloat]
Dataframe = pd.DataFrame
Series = pd.Series
