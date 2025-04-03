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
from outquantlab.structures import arrays, consts


def ratio_normalization(nominator: arrays.Float2D, denominator: arrays.Float2D) -> arrays.Float2D:
    return (nominator / denominator) - consts.ONE


def sign_normalization(signal_array: arrays.Float2D) -> arrays.Float2D:
    return sign(signal_array, out=signal_array)

def long_bias_normalization(signal_array: arrays.Float2D) -> arrays.Float2D:
    return where(signal_array > consts.ZERO, signal_array, consts.ZERO)


def relative_normalization(signal_array: arrays.Float2D, length: int) -> arrays.Float2D:
    return signal_array - get_rolling_mean(
        array=signal_array, length=length, min_length=1
    )


def z_score_normalization(signal_array: arrays.Float2D, length: int) -> arrays.Float2D:
    return relative_normalization(
        signal_array=signal_array, length=length
    ) / get_rolling_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: arrays.Float2D, limit: int = 1) -> arrays.Float2D:
    return clip(signal_array, -limit, limit)


def get_indicator_on_trend_signal(
    trend_signal: arrays.Float2D, indicator_signal: arrays.Float2D
) -> arrays.Float2D:
    return where(
        ((trend_signal < consts.ZERO) & (indicator_signal > consts.ZERO))
        | ((trend_signal > consts.ZERO) & (indicator_signal < consts.ZERO)),
        consts.ZERO,
        indicator_signal,
    )


def get_rolling_median_normalisation(
    signal_array: arrays.Float2D, window_length: int
) -> arrays.Float2D:
    median_array: arrays.Float2D = get_rolling_median(
        array=signal_array, length=window_length, min_length=window_length
    )
    max_array: arrays.Float2D = get_rolling_max(
        array=signal_array, length=window_length, min_length=window_length
    )
    min_array: arrays.Float2D = get_rolling_min(
        array=signal_array, length=window_length, min_length=window_length
    )

    return ((signal_array - median_array) / (max_array - min_array)) * arrays.Float32(2.0)


def rolling_scalar_normalisation(raw_signal: arrays.Float2D, limit: int = 2) -> arrays.Float2D:
    scalar: arrays.Float2D = _get_normalized_scalar(raw_signal=raw_signal)
    reshaped_scalar: arrays.Float2D = scalar.reshape(-1, 1)
    normalized_signal: arrays.Float2D = reshaped_scalar * raw_signal
    return limit_normalization(signal_array=normalized_signal, limit=limit)


def dynamic_signal(
    metric: arrays.Float2D,
    signal: arrays.Float2D,
    comparator: Callable[[arrays.Float2D, arrays.Float32], arrays.Float2D] = gt,
) -> arrays.Float2D:
    return where(comparator(metric, consts.ZERO), -signal, signal)


def _get_normalized_scalar(
    raw_signal: arrays.Float2D, length: int = consts.YEAR, target: int = 1
) -> arrays.Float2D:
    median: arrays.Float2D = get_overall_median(array=absolute(raw_signal), axis=1)
    mean: arrays.Float2D = get_rolling_mean(
        array=median, length=raw_signal.shape[0], min_length=length
    )
    scalar: arrays.Float2D = target / mean
    return arrays.backfill(array=scalar)