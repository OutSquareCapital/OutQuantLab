from numbagg import bfill
from numpy import (
    append,
    arange,
    argsort,
    concatenate,
    cumprod,
    empty,
    empty_like,
    full_like,
    full,
    isnan,
    log,
    logical_or
)
from outquantlab.structures.arrays.types import (
    ArrayFloat,
    Float32,
    Nan,
    ArrayInt
)



def empty_array(shape: tuple[int, ...]) -> ArrayFloat:
    return empty(shape=shape, dtype=Float32)

def empty_array_like(model: ArrayFloat) -> ArrayFloat:
    return empty_like(prototype=model, dtype=Float32)

def full_array(shape: tuple[int, ...], fill_value: float) -> ArrayFloat:
    return full(shape=shape, fill_value=fill_value, dtype=Float32)

def full_array_like(model: ArrayFloat, fill_value: float) -> ArrayFloat:
    return full_like(a=model, fill_value=fill_value, dtype=Float32)

def nan_array(shape: tuple[int, ...]) -> ArrayFloat:
    return full(shape=shape, fill_value=Nan, dtype=Float32)

def nan_array_like(model: ArrayFloat) -> ArrayFloat:
    return full_like(a=model, fill_value=Nan, dtype=Float32)

def reduce_array(array: ArrayFloat, frequency: int) -> ArrayFloat:
    array_length: int = array.shape[0]
    indices: ArrayInt = arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        selected_indices: ArrayInt = append(arr=indices, values=array_length - 1)
        return array[selected_indices]
    return array[indices]


def log_returns_array(prices_array: ArrayFloat) -> ArrayFloat:
    ratios = prices_array[1:] / prices_array[:-1]
    log_returns_array: ArrayFloat = empty_array_like(model=prices_array)
    log_returns_array[0] = Nan
    log_returns_array[1:] = log(ratios)
    return log_returns_array


def pct_returns_array(prices_array: ArrayFloat) -> ArrayFloat:
    pct_returns_array: ArrayFloat = empty_array_like(model=prices_array)
    pct_returns_array[0] = Nan
    pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    return pct_returns_array


def get_prices_array(returns_array: ArrayFloat) -> ArrayFloat:
    temp_array: ArrayFloat = returns_array.copy()
    mask: ArrayFloat = isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns: ArrayFloat = empty_array_like(model=temp_array)

    cumulative_returns[:0] = Nan

    cumulative_returns[0:] = cumprod(a=1 + temp_array[0:], axis=0)

    cumulative_returns[mask] = Nan

    return cumulative_returns * Float32(100)


def shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_array_like(model=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = Nan
    return shifted_array


def combine_arrays(arrays_list: list[ArrayFloat]) -> ArrayFloat:
    return concatenate([array.reshape(1) for array in arrays_list])


def backfill_array(array: ArrayFloat) -> ArrayFloat:
    return bfill(array, axis=0)  # type: ignore

def fill_nan_array(array: ArrayFloat) -> ArrayFloat:
    result_array: ArrayFloat = array.copy()
    finite_mask: ArrayFloat = isnan(array)
    cumulative_valid: ArrayFloat = logical_or.accumulate(array=finite_mask, axis=0)
    fill_mask: ArrayFloat = isnan(array) & cumulative_valid
    result_array[fill_mask] = 0
    return result_array

def get_sorted_indices(array: ArrayFloat, ascending: bool) -> ArrayInt:
    sorted_indices: ArrayInt = argsort(array)
    if not ascending:
        sorted_indices = sorted_indices[::-1]
    return sorted_indices