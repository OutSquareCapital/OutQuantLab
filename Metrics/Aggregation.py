import bottleneck as bn  # type: ignore
import numpy as np
import polars as pl
from numpy.typing import NDArray


def rolling_mean(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    return bn.move_mean(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_median(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    return bn.move_median(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_max(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    return bn.move_max(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_min(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    return bn.move_min(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_central(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    upper = rolling_max(array, length=length, min_length=min_length)
    lower = rolling_min(array, length=length, min_length=min_length)
    return (upper + lower) / 2

def rolling_sum(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:
    return bn.move_sum(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_weighted_mean(array: NDArray[np.float32], length: int) -> NDArray[np.float32]:
    wma_array = np.full(array.shape, np.nan, dtype=np.float32)
    weights = np.arange(1, length + 1, dtype=np.float32)
    weight_sum = weights.sum()
    weighted_sum = np.apply_along_axis(lambda x: np.convolve(x, weights[::-1], mode='valid'), axis=0, arr=array)
    wma_array[length - 1:] = weighted_sum / weight_sum
    return wma_array

def rolling_quantile_ratio(returns_array: NDArray[np.float32], window: int, quantile_spread: float) -> NDArray[np.float32]:
    quantile_low = 0.5 - quantile_spread
    quantile_high = 0.5 + quantile_spread
    df = pl.DataFrame(returns_array).with_columns([
        pl.all().fill_nan(None)
    ])
    quantile_low_values = df.select(
        pl.all().rolling_quantile(quantile=quantile_low, window_size=window, min_periods=window)
    )
    quantile_high_values = df.select(
        pl.all().rolling_quantile(quantile=quantile_high, window_size=window, min_periods=window)
    )
    quantile_low_values_array = quantile_low_values.to_numpy()
    quantile_high_values_array = quantile_high_values.to_numpy()
    return (quantile_high_values_array + quantile_low_values_array) / 2
