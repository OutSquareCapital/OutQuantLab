import bottleneck as bn  # type: ignore
import polars as pl

from outquantlab.structures import arrays


def get_overall_mean(
    array: arrays.ArrayFloat, axis: None | int = 0
) -> arrays.ArrayFloat:
    return bn.nanmean(array, axis)  # type: ignore


def get_overall_median(
    array: arrays.ArrayFloat, axis: None | int = 0
) -> arrays.ArrayFloat:
    return bn.nanmedian(array, axis)  # type: ignore


def get_rolling_mean(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_mean(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_rolling_median(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_median(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_overall_max(array: arrays.ArrayFloat, axis: int = 0) -> arrays.ArrayFloat:
    return bn.nanmax(array, axis)  # type: ignore


def get_overall_min(array: arrays.ArrayFloat, axis: int = 0) -> arrays.ArrayFloat:
    return bn.nanmin(array, axis)  # type: ignore


def get_rolling_max(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_max(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_rolling_min(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_min(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_rolling_central(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    upper: arrays.ArrayFloat = get_rolling_max(
        array=array, length=length, min_length=min_length
    )
    lower: arrays.ArrayFloat = get_rolling_min(
        array=array, length=length, min_length=min_length
    )
    return (upper + lower) / 2


def get_rolling_sum(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_sum(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_rolling_quantile_ratio(
    returns_array: arrays.ArrayFloat, window: int, quantile_spread: float
) -> arrays.ArrayFloat:
    quantile_low: float = 0.5 - quantile_spread
    quantile_high: float = 0.5 + quantile_spread
    df: pl.DataFrame = pl.DataFrame(data=returns_array).with_columns(
        [pl.all().fill_nan(value=None)]
    )
    quantile_low_values: pl.DataFrame = df.select(
        pl.all().rolling_quantile(
            quantile=quantile_low, window_size=window, min_periods=window
        )
    )
    quantile_high_values: pl.DataFrame = df.select(
        pl.all().rolling_quantile(
            quantile=quantile_high, window_size=window, min_periods=window
        )
    )
    quantile_low_values_array: arrays.ArrayFloat = quantile_low_values.to_numpy()
    quantile_high_values_array: arrays.ArrayFloat = quantile_high_values.to_numpy()
    return (quantile_high_values_array + quantile_low_values_array) / 2
