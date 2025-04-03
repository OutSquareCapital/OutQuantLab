from collections.abc import Callable
from operator import gt

from numpy import clip, sign, where, absolute

from outquantlab.metrics.aggregation import (
    get_overall_median,
    get_rolling_max,
    get_rolling_mean,
    get_rolling_median,
    get_rolling_min,
)
from outquantlab.metrics.volatility import get_rolling_volatility
from outquantlab.metrics.maths_constants import TimePeriod, ZERO, ONE
from outquantlab.structures import arrays


def ratio_normalization(nominator: arrays.ArrayFloat, denominator: arrays.ArrayFloat) -> arrays.ArrayFloat:
    return (nominator / denominator) - ONE


def sign_normalization(signal_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    return sign(signal_array, out=signal_array)

def long_bias_normalization(signal_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    return where(signal_array > ZERO, signal_array, ZERO)


def relative_normalization(signal_array: arrays.ArrayFloat, length: int) -> arrays.ArrayFloat:
    return signal_array - get_rolling_mean(
        array=signal_array, length=length, min_length=1
    )


def z_score_normalization(signal_array: arrays.ArrayFloat, length: int) -> arrays.ArrayFloat:
    return relative_normalization(
        signal_array=signal_array, length=length
    ) / get_rolling_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: arrays.ArrayFloat, limit: int = 1) -> arrays.ArrayFloat:
    return clip(signal_array, -limit, limit)


def get_indicator_on_trend_signal(
    trend_signal: arrays.ArrayFloat, indicator_signal: arrays.ArrayFloat
) -> arrays.ArrayFloat:
    return where(
        ((trend_signal < ZERO) & (indicator_signal > ZERO))
        | ((trend_signal > ZERO) & (indicator_signal < ZERO)),
        ZERO,
        indicator_signal,
    )


def get_rolling_median_normalisation(
    signal_array: arrays.ArrayFloat, window_length: int
) -> arrays.ArrayFloat:
    median_array: arrays.ArrayFloat = get_rolling_median(
        array=signal_array, length=window_length, min_length=window_length
    )
    max_array: arrays.ArrayFloat = get_rolling_max(
        array=signal_array, length=window_length, min_length=window_length
    )
    min_array: arrays.ArrayFloat = get_rolling_min(
        array=signal_array, length=window_length, min_length=window_length
    )

    return ((signal_array - median_array) / (max_array - min_array)) * arrays.Float32(2.0)


def rolling_scalar_normalisation(raw_signal: arrays.ArrayFloat, limit: int = 2) -> arrays.ArrayFloat:
    scalar: arrays.ArrayFloat = _get_normalized_scalar(raw_signal=raw_signal)
    reshaped_scalar: arrays.ArrayFloat = scalar.reshape(-1, 1)
    normalized_signal: arrays.ArrayFloat = reshaped_scalar * raw_signal
    return limit_normalization(signal_array=normalized_signal, limit=limit)


def dynamic_signal(
    metric: arrays.ArrayFloat,
    signal: arrays.ArrayFloat,
    comparator: Callable[[arrays.ArrayFloat, arrays.Float32], arrays.ArrayFloat] = gt,
) -> arrays.ArrayFloat:
    return where(comparator(metric, ZERO), -signal, signal)


def _get_normalized_scalar(
    raw_signal: arrays.ArrayFloat, length: int = TimePeriod.YEAR, target: int = 1
) -> arrays.ArrayFloat:
    median: arrays.ArrayFloat = get_overall_median(array=absolute(raw_signal), axis=1)
    mean: arrays.ArrayFloat = get_rolling_mean(
        array=median, length=raw_signal.shape[0], min_length=length
    )
    scalar: arrays.ArrayFloat = target / mean
    return arrays.backfill_array(array=scalar)