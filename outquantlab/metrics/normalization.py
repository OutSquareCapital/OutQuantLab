from collections.abc import Callable
import numpy as np
from operator import gt

from outquantlab.metrics.aggregation import (
    rolling_mean,
    rolling_median,
    rolling_min,
    rolling_max,
)
from outquantlab.metrics.volatility import rolling_volatility
from outquantlab.typing_conventions import ArrayFloat, Float32



def ratio_normalization(nominator: ArrayFloat, denominator: ArrayFloat) -> ArrayFloat:
    return (nominator / denominator) - Float32(1.0)


def sign_normalization(signal_array: ArrayFloat) -> ArrayFloat:
    return np.sign(signal_array, out=signal_array)


def relative_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    return signal_array - rolling_mean(array=signal_array, length=length, min_length=1)


def z_score_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    return relative_normalization(
        signal_array=signal_array, length=length
    ) / rolling_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: ArrayFloat, limit: int = 1) -> ArrayFloat:
    return np.clip(signal_array, -limit, limit)


def calculate_indicator_on_trend_signal(
    trend_signal: ArrayFloat, indicator_signal: ArrayFloat
) -> ArrayFloat:
    limit: Float32 = Float32(0.0)
    return np.where(
        ((trend_signal < limit) & (indicator_signal > limit))
        | ((trend_signal > limit) & (indicator_signal < limit)),
        limit,
        indicator_signal,
    )


def rolling_median_normalisation(
    signal_array: ArrayFloat, window_length: int
) -> ArrayFloat:
    median_array: ArrayFloat = rolling_median(
        array=signal_array, length=window_length, min_length=window_length
    )
    max_array: ArrayFloat = rolling_max(
        array=signal_array, length=window_length, min_length=window_length
    )
    min_array: ArrayFloat = rolling_min(
        array=signal_array, length=window_length, min_length=window_length
    )

    return ((signal_array - median_array) / (max_array - min_array)) * Float32(2.0)


def dynamic_signal(
    metric: ArrayFloat,
    signal: ArrayFloat,
    comparaison: Callable[[ArrayFloat, Float32], ArrayFloat] = gt,
) -> ArrayFloat:
    return np.where(comparaison(metric, Float32(0.0)), -signal, signal)
