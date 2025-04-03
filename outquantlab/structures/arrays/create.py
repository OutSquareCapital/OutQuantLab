import numpy as np

from outquantlab.structures.arrays.types import Float2D, Float32, Int2D, Nan


def empty(shape: tuple[int, ...]) -> Float2D:
    return np.empty(shape=shape, dtype=Float32)


def empty_like(model: Float2D) -> Float2D:
    return np.empty_like(prototype=model, dtype=Float32)


def full(shape: tuple[int, ...], fill_value: float) -> Float2D:
    return np.full(shape=shape, fill_value=fill_value, dtype=Float32)


def full_like(model: Float2D, fill_value: float) -> Float2D:
    return np.full_like(a=model, fill_value=fill_value, dtype=Float32)


def create_nan(shape: tuple[int, ...]) -> Float2D:
    return np.full(shape=shape, fill_value=Nan, dtype=Float32)


def nan_like(model: Float2D) -> Float2D:
    return np.full_like(a=model, fill_value=Nan, dtype=Float32)


def get_sorted_indices(array: Float2D, ascending: bool) -> Int2D:
    sorted_indices: Int2D = np.argsort(array)
    if not ascending:
        sorted_indices = sorted_indices[::-1]
    return sorted_indices
