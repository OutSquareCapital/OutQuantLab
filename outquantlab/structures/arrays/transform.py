import numpy as np
from numbagg import bfill

from outquantlab.structures.arrays.create import empty_like
from outquantlab.structures.arrays.types import Float2D, Float32, Int2D, Nan


def reduce(array: Float2D, frequency: int) -> Float2D:
    array_length: int = array.shape[0]
    indices: Int2D = np.arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        selected_indices: Int2D = np.append(arr=indices, values=array_length - 1)
        return array[selected_indices]
    return array[indices]


def log_returns(prices: Float2D) -> Float2D:
    ratios = prices[1:] / prices[:-1]
    log_returns: Float2D = empty_like(model=prices)
    log_returns[0] = Nan
    log_returns[1:] = np.log(ratios)
    return log_returns


def pct_returns(prices: Float2D) -> Float2D:
    pct_returns: Float2D = empty_like(model=prices)
    pct_returns[0] = Nan
    pct_returns[1:] = prices[1:] / prices[:-1] - 1
    return pct_returns


def get_prices(returns: Float2D) -> Float2D:
    temp: Float2D = returns.copy()
    mask: Float2D = np.isnan(temp)
    temp[mask] = 0

    cumulative_returns: Float2D = empty_like(model=temp)

    cumulative_returns[:0] = Nan

    cumulative_returns[0:] = np.cumprod(a=1 + temp[0:], axis=0)

    cumulative_returns[mask] = Nan

    return cumulative_returns * Float32(100)


def shift(original: Float2D, step: int = 1) -> Float2D:
    shifted: Float2D = empty_like(model=original)
    shifted[step:, :] = original[:-step, :]
    shifted[:step, :] = Nan
    return shifted


def combine(arrays_list: list[Float2D]) -> Float2D:
    return np.concatenate([array.reshape(1) for array in arrays_list])


def backfill(array: Float2D) -> Float2D:
    return bfill(array, axis=0)  # type: ignore


def fill_nan(array: Float2D) -> Float2D:
    result: Float2D = array.copy()
    finite_mask: Float2D = np.isnan(array)
    cumulative_valid: Float2D = np.logical_or.accumulate(array=finite_mask, axis=0)
    fill_mask: Float2D = np.isnan(array) & cumulative_valid
    result[fill_mask] = 0
    return result