from collections.abc import Callable
from operator import gt

import numbagg as nb
from numpy import clip, sign, where, quantile, nan

from outquantlab.metrics.aggregation import (
    get_overall_median,
    get_rolling_max,
    get_rolling_mean,
    get_rolling_median,
    get_rolling_min,
)
from outquantlab.metrics.volatility import get_rolling_volatility
from outquantlab.metrics.maths_constants import PERCENTAGE_FACTOR
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
    ) / get_rolling_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: ArrayFloat, limit: int = 1) -> ArrayFloat:
    return clip(signal_array, -limit, limit)


def get_indicator_on_trend_signal(
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


def rolling_scalar_normalisation(raw_signal: ArrayFloat, limit: int = 2) -> ArrayFloat:
    scalar: ArrayFloat = _get_normalized_scalar(raw_signal=raw_signal)
    reshaped_scalar: ArrayFloat = scalar.reshape(-1, 1)
    normalized_signal: ArrayFloat = reshaped_scalar * raw_signal
    return limit_normalization(signal_array=normalized_signal, limit=limit)


def dynamic_signal(
    metric: ArrayFloat,
    signal: ArrayFloat,
    comparator: Callable[[ArrayFloat, Float32], ArrayFloat] = gt,
) -> ArrayFloat:
    return where(comparator(metric, Float32(0.0)), -signal, signal)


def _get_normalized_scalar(
    raw_signal: ArrayFloat, length: int = 500, target: int = 1
) -> ArrayFloat:
    median: ArrayFloat = get_overall_median(array=abs(raw_signal), axis=1)
    mean: ArrayFloat = get_rolling_mean(
        array=median, length=raw_signal.shape[0], min_length=length
    )
    scalar: ArrayFloat = target / mean
    return _bfill(array=scalar)


def _bfill(array: ArrayFloat) -> ArrayFloat:
    return nb.bfill(array, axis=0)  # type: ignore


def get_returns_distribution(returns_array: ArrayFloat, limit: int) -> ArrayFloat:
    treshold: float = limit/100
    lower_threshold: ArrayFloat = quantile(a=returns_array, q=treshold, axis=0)
    upper_threshold: ArrayFloat = quantile(a=returns_array, q=1 - treshold, axis=0)

    limited_returns_array: ArrayFloat = where(
        (returns_array >= lower_threshold) & (returns_array <= upper_threshold),
        returns_array,
        nan,
    )

    return limited_returns_array * PERCENTAGE_FACTOR
