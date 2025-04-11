from numquant.arrays import backfill
from numquant.main import Float2D, Float32, np
from numquant.metrics.aggregate import get_median as get_median_agg
from numquant.metrics.constants import ONE, ZERO, Period
from numquant.metrics.rolling.main import (
    get_expanding_mean,
    get_max,
    get_mean,
    get_median,
    get_min,
)
from numquant.metrics.rolling.volatility import get_volatility

# TODO: virer toutes les fonctions qui sont indicateurs et pas ultra genériques


def ratio_normalization(nominator: Float2D, denominator: Float2D) -> Float2D:
    return (nominator / denominator) - ONE


def sign_normalization(signal_array: Float2D) -> Float2D:
    return np.sign(signal_array, out=signal_array)


def long_bias_normalization(signal_array: Float2D) -> Float2D:
    return np.where(signal_array > ZERO, signal_array, ZERO)


def short_bias_normalization(signal_array: Float2D) -> Float2D:
    return np.where(signal_array < ZERO, signal_array, ZERO)


def relative_normalization(signal_array: Float2D, length: int) -> Float2D:
    return signal_array - get_mean(array=signal_array, length=length, min_length=1)


def z_score_normalization(signal_array: Float2D, length: int) -> Float2D:
    return relative_normalization(
        signal_array=signal_array, length=length
    ) / get_volatility(array=signal_array, length=length, min_length=1)


def limit_normalization(signal_array: Float2D, limit: int = 1) -> Float2D:
    return np.clip(signal_array, -limit, limit)


def get_indicator_on_trend_signal(
    trend_signal: Float2D, indicator_signal: Float2D
) -> Float2D:
    return np.where(
        ((trend_signal < ZERO) & (indicator_signal > ZERO))
        | ((trend_signal > ZERO) & (indicator_signal < ZERO)),
        ZERO,
        indicator_signal,
    )


def get_median_normalisation(signal_array: Float2D, window_length: int) -> Float2D:
    median_array: Float2D = get_median(
        array=signal_array, length=window_length, min_length=window_length
    )
    max_array: Float2D = get_max(
        array=signal_array, length=window_length, min_length=window_length
    )
    min_array: Float2D = get_min(
        array=signal_array, length=window_length, min_length=window_length
    )

    return ((signal_array - median_array) / (max_array - min_array)) * Float32(2.0)


def rolling_scalar_normalisation(raw_signal: Float2D, limit: int = 2) -> Float2D:
    scalar: Float2D = _get_normalized_scalar(raw_signal=raw_signal)
    reshaped_scalar: Float2D = scalar.reshape(-1, 1)
    normalized_signal: Float2D = reshaped_scalar * raw_signal
    return limit_normalization(signal_array=normalized_signal, limit=limit)


def invert_signal_long(
    metric: Float2D,
    signal: Float2D,
) -> Float2D:
    return np.where(metric > ZERO, -signal, signal)


def invert_signal_short(
    metric: Float2D,
    signal: Float2D,
) -> Float2D:
    return np.where(metric < ZERO, -signal, signal)


def _get_normalized_scalar(
    raw_signal: Float2D, length: int = Period.YEAR, target: int = 1
) -> Float2D:
    median: Float2D = get_median_agg(array=np.abs(raw_signal), axis=1)
    mean: Float2D = get_expanding_mean(array=median, min_length=length)
    scalar: Float2D = (
        target / mean
    )  # TODO: trouver une solution pour les actifs/strategies qui ont des periodes de 0
    return backfill(array=scalar)
