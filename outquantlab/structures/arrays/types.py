from typing import TypeAlias

import numpy as np

Nan: float = np.nan
Float32: TypeAlias = np.float32
Int32: TypeAlias = np.int32


Int1D: TypeAlias = np.ndarray[tuple[int], np.dtype[Int32]]
Int2D: TypeAlias = np.ndarray[tuple[int, int], np.dtype[Int32]]
Float1D: TypeAlias = np.ndarray[tuple[int], np.dtype[Float32]]
Float2D: TypeAlias = np.ndarray[tuple[int, int], np.dtype[Float32]]
