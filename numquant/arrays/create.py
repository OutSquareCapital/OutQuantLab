from numba import njit # type: ignore
from numquant.main import Float2D, Float32, Nan, np, Float1D

@njit
def create_1dim(data: tuple[float, ...]) -> Float1D:
    return np.array(data, dtype=Float32)

@njit
def create_2dim(data: tuple[tuple[float, ...], ...]) -> Float2D:
    return np.array(data, dtype=Float32)

@njit
def create_empty(length: int, width: int) -> Float2D:
    return np.empty(shape=(length, width), dtype=Float32)

@njit
def create_empty_like(model: Float2D) -> Float2D:
    return np.empty_like(model, dtype=Float32)

@njit
def create_full(length: int, width: int, fill_value: Float32) -> Float2D:
    return np.full(shape=(length, width), fill_value=fill_value, dtype=Float32)

@njit
def create_full_like(model: Float2D, fill_value: Float32) -> Float2D:
    return np.full_like(model, fill_value=fill_value, dtype=Float32)

@njit
def create_nan(length: int, width: int) -> Float2D:
    return np.full(shape=(length, width), fill_value=Nan, dtype=Float32)

@njit
def create_nan_like(model: Float2D) -> Float2D:
    return np.full_like(model, fill_value=Nan, dtype=Float32)