from numpy.typing import NDArray
import numpy as np
from collections.abc import Callable
from typing import Any, TypeAlias, Final

ArrayFloat: TypeAlias = NDArray[np.float32]
ArrayInt: TypeAlias = NDArray[np.int32]
ProgressFunc: TypeAlias = Callable[[int, str], Any]
IndicatorFunc : TypeAlias = Callable[..., ArrayFloat]

JsonData: TypeAlias = str
ParquetData: TypeAlias = str
WebpMedia: TypeAlias = str
PngMedia: TypeAlias = str
JSON_EXT: Final = ".json"
PARQUET_EXT: Final = ".parquet"
WEBP_EXT: Final = ".webp"
PNG_EXT: Final = ".png"