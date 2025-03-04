from collections.abc import Callable
from operator import gt

import numbagg as nb
from numpy import clip, sign, where

from outquantlab.metrics.aggregation import (
    get_overall_median,
    get_rolling_max,
    get_rolling_mean,
    get_rolling_median,
    get_rolling_min,
)
from outquantlab.metrics.volatility import rolling_volatility
from outquantlab.typing_conventions import (
    ArrayFloat,
    Float32,
)


def ratio_normalization(nominator: ArrayFloat, denominator: ArrayFloat) -> ArrayFloat:
    return (nominator / denominator) - Float32(1.0)


def sign_normalization(signal_array: ArrayFloat) -> ArrayFloat:
    return sign(signal_array, out=signal_array)


def relative_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    return signal_array - get_rolling_mean(
        array=signal_array, length=length, min_length=1
    )


def z_score_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    return relative_normalization(
        signal_array=signal_array, length=length
    ) / rolling_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: ArrayFloat, limit: int = 1) -> ArrayFloat:
    return clip(signal_array, -limit, limit)


def calculate_indicator_on_trend_signal(
    trend_signal: ArrayFloat, indicator_signal: ArrayFloat
) -> ArrayFloat:
    limit: Float32 = Float32(0.0)
    return where(
        ((trend_signal < limit) & (indicator_signal > limit))
        | ((trend_signal > limit) & (indicator_signal < limit)),
        limit,
        indicator_signal,
    )


def get_rolling_median_normalisation(
    signal_array: ArrayFloat, window_length: int
) -> ArrayFloat:
    median_array: ArrayFloat = get_rolling_median(
        array=signal_array, length=window_length, min_length=window_length
    )
    max_array: ArrayFloat = get_rolling_max(
        array=signal_array, length=window_length, min_length=window_length
    )
    min_array: ArrayFloat = get_rolling_min(
        array=signal_array, length=window_length, min_length=window_length
    )

    return ((signal_array - median_array) / (max_array - min_array)) * Float32(2.0)


def rolling_scalar_normalisation(
    data: ArrayFloat, length: int = 500, target: int = 1, limit: int = 20
) -> ArrayFloat:
    median: ArrayFloat = get_overall_median(array=abs(data), axis=1)
    mean: ArrayFloat = get_rolling_mean(
        array=median, length=data.shape[0], min_length=length
    )
    scalar: ArrayFloat = target / mean
    filled_scalar: ArrayFloat = _bfill(array=scalar)
    reshaped_scalar: ArrayFloat = filled_scalar.reshape(-1, 1)
    return limit_normalization(signal_array=reshaped_scalar, limit=limit)


def dynamic_signal(
    metric: ArrayFloat,
    signal: ArrayFloat,
    comparator: Callable[[ArrayFloat, Float32], ArrayFloat] = gt,
) -> ArrayFloat:
    return where(comparator(metric, Float32(0.0)), -signal, signal)


def _bfill(array: ArrayFloat) -> ArrayFloat:
    return nb.bfill(array, axis=0)  # type: ignore
