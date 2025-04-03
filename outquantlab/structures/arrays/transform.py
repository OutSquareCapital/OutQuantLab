import numpy as np
from numbagg import bfill

from outquantlab.structures.arrays.create import empty_array_like
from outquantlab.structures.arrays.types import Float2D, Float32, Int2D, Nan


def reduce_array(array: Float2D, frequency: int) -> Float2D:
    array_length: int = array.shape[0]
    indices: Int2D = np.arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        selected_indices: Int2D = np.append(arr=indices, values=array_length - 1)
        return array[selected_indices]
    return array[indices]


def log_returns_array(prices_array: Float2D) -> Float2D:
    ratios = prices_array[1:] / prices_array[:-1]
    log_returns_array: Float2D = empty_array_like(model=prices_array)
    log_returns_array[0] = Nan
    log_returns_array[1:] = np.log(ratios)
    return log_returns_array


def pct_returns_array(prices_array: Float2D) -> Float2D:
    pct_returns_array: Float2D = empty_array_like(model=prices_array)
    pct_returns_array[0] = Nan
    pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    return pct_returns_array


def get_prices_array(returns_array: Float2D) -> Float2D:
    temp_array: Float2D = returns_array.copy()
    mask: Float2D = np.isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns: Float2D = empty_array_like(model=temp_array)

    cumulative_returns[:0] = Nan

    cumulative_returns[0:] = np.cumprod(a=1 + temp_array[0:], axis=0)

    cumulative_returns[mask] = Nan

    return cumulative_returns * Float32(100)


def shift_array(original_array: Float2D, step: int = 1) -> Float2D:
    shifted_array: Float2D = empty_array_like(model=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = Nan
    return shifted_array


def combine_arrays(arrays_list: list[Float2D]) -> Float2D:
    return np.concatenate([array.reshape(1) for array in arrays_list])


def backfill_array(array: Float2D) -> Float2D:
    return bfill(array, axis=0)  # type: ignore


def fill_nan_array(array: Float2D) -> Float2D:
    result_array: Float2D = array.copy()
    finite_mask: Float2D = np.isnan(array)
    cumulative_valid: Float2D = np.logical_or.accumulate(array=finite_mask, axis=0)
    fill_mask: Float2D = np.isnan(array) & cumulative_valid
    result_array[fill_mask] = 0
    return result_array


__all__: list[str] = [
    "backfill_array",
    "combine_arrays",
    "fill_nan_array",
    "get_prices_array",
    "log_returns_array",
    "pct_returns_array",
    "reduce_array",
    "shift_array",
]
