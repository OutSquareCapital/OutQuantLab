import bottleneck as bn  # type: ignore
import numpy as np
import polars as pl
from Utilitary import ArrayFloat, Float32

def calculate_overall_mean(array: ArrayFloat, axis: int = 0) -> ArrayFloat:
    return bn.nanmean(array, axis) # type: ignore

def rolling_mean(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_mean(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_median(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_median(array, window=length, min_count=min_length, axis=0) # type: ignore

def calculate_overall_max(array: ArrayFloat, axis: int = 0) -> ArrayFloat:
    return np.nanmax(array, axis=axis)

def rolling_max(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_max(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_min(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_min(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_central(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    upper = rolling_max(array, length=length, min_length=min_length)
    lower = rolling_min(array, length=length, min_length=min_length)
    return (upper + lower) / 2

def rolling_sum(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_sum(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_weighted_mean(array: ArrayFloat, length: int) -> ArrayFloat:
    def convolve_with_weights(x: ArrayFloat, weights: ArrayFloat) -> ArrayFloat:
        return np.convolve(x, weights[::-1], mode='valid')

    wma_array = np.full(array.shape, np.nan, dtype=Float32)
    weights = np.arange(1, length + 1, dtype=Float32)
    weight_sum = weights.sum()
    weighted_sum = np.apply_along_axis(convolve_with_weights, axis=0, arr=array, weights=weights)
    wma_array[length - 1:] = weighted_sum / weight_sum
    return wma_array

def rolling_quantile_ratio(returns_array: ArrayFloat, window: int, quantile_spread: float) -> ArrayFloat:
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
