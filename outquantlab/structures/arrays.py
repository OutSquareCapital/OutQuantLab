from typing import TypeAlias

from numbagg import bfill
from numpy import (
    NAN,
    append,
    arange,
    argsort,
    concatenate,
    cumprod,
    empty,
    empty_like,
    float32,
    full,
    int32,
    isnan,
    log,
)
from numpy.typing import NDArray

Nan: float = NAN
Float32: TypeAlias = float32
Int32: TypeAlias = int32
ArrayFloat: TypeAlias = NDArray[Float32]
ArrayInt: TypeAlias = NDArray[Int32]


def empty_array(shape: tuple[int, ...]) -> ArrayFloat:
    return empty(shape=shape, dtype=Float32)


def full_array(shape: tuple[int, ...], fill_value: float) -> ArrayFloat:
    return full(shape=shape, fill_value=fill_value, dtype=Float32)


def empty_like_array(prototype: ArrayFloat) -> ArrayFloat:
    return empty_like(prototype=prototype, dtype=Float32)


def reduce_array(array: ArrayFloat, frequency: int) -> ArrayFloat:
    array_length: int = array.shape[0]
    indices: ArrayInt = arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        selected_indices: ArrayInt = append(arr=indices, values=array_length - 1)
        return array[selected_indices]
    return array[indices]


def log_returns_array(prices_array: ArrayFloat) -> ArrayFloat:
    ratios = prices_array[1:] / prices_array[:-1]
    log_returns_array: ArrayFloat = empty_like_array(prototype=prices_array)
    log_returns_array[0] = Nan
    log_returns_array[1:] = log(ratios)
    return log_returns_array


def pct_returns_array(prices_array: ArrayFloat) -> ArrayFloat:
    pct_returns_array: ArrayFloat = empty_like_array(prototype=prices_array)
    pct_returns_array[0] = Nan
    pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    return pct_returns_array


def get_prices_array(returns_array: ArrayFloat) -> ArrayFloat:
    temp_array: ArrayFloat = returns_array.copy()
    mask: ArrayFloat = isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns: ArrayFloat = empty_like_array(prototype=temp_array)

    cumulative_returns[:0] = Nan

    cumulative_returns[0:] = cumprod(a=1 + temp_array[0:], axis=0)

    cumulative_returns[mask] = Nan

    return cumulative_returns * Float32(100)


def shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_like_array(prototype=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = Nan
    return shifted_array


def combine_arrays(arrays_list: list[ArrayFloat]) -> ArrayFloat:
    return concatenate([array.reshape(1) for array in arrays_list])


def backfill_array(array: ArrayFloat) -> ArrayFloat:
    return bfill(array, axis=0)  # type: ignore


def get_sorted_indices(array: ArrayFloat, ascending: bool) -> ArrayInt:
    sorted_indices: ArrayInt = argsort(array)
    if not ascending:
        sorted_indices = sorted_indices[::-1]
    return sorted_indices
