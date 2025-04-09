import numpy as np
from numba import njit # type: ignore
from outquantlab.structures.arrays.types import Float2D, Float32, Nan

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

def create_from_list(arrays_list: list[Float2D]) -> Float2D:
    return np.concatenate([array.reshape(1) for array in arrays_list])
