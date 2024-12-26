from numpy.typing import NDArray
import numpy as np
import pandas as pd
from collections.abc import Callable

NDArrayFloat = NDArray[np.float32]
IndicatorFunc = Callable[[list[int]], NDArrayFloat]
Dataframe = pd.DataFrame
Series = pd.Series
