import bottleneck as bn  # type: ignore
import polars as pl
from typing_conventions import ArrayFloat

def calculate_overall_mean(array: ArrayFloat, axis: None|int = 0) -> ArrayFloat:
    return bn.nanmean(array, axis) # type: ignore

def rolling_mean(array: ArrayFloat, length: int, min_length: int) -> ArrayFloat:
    return bn.move_mean(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_median(array: ArrayFloat, length: int, min_length: int) -> ArrayFloat:
    return bn.move_median(array, window=length, min_count=min_length, axis=0) # type: ignore

def calculate_overall_max(array: ArrayFloat, axis: int = 0) -> ArrayFloat:
    return bn.nanmax(array, axis) # type: ignore

def calculate_overall_min(array: ArrayFloat, axis: int = 0) -> ArrayFloat:
    return bn.nanmin(array, axis) # type: ignore

def rolling_max(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_max(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_min(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_min(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_central(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    upper: ArrayFloat = rolling_max(array=array, length=length, min_length=min_length)
    lower: ArrayFloat = rolling_min(array=array, length=length, min_length=min_length)
    return (upper + lower) / 2

def rolling_sum(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_sum(array, window=length, min_count=min_length, axis=0) # type: ignore

def rolling_quantile_ratio(returns_array: ArrayFloat, window: int, quantile_spread: float) -> ArrayFloat:
    quantile_low: float = 0.5 - quantile_spread
    quantile_high: float = 0.5 + quantile_spread
    df: pl.DataFrame = pl.DataFrame(data=returns_array).with_columns([
        pl.all().fill_nan(value=None)
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
