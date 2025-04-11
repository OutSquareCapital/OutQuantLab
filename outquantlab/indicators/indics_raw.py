from outquantlab.indicators.params_types import (
    Acceleration,
    SmoothedSignal,
    Trend,
    Volatility,
    NormalizedSmoothedSignal
)
import numquant as nq


def get_mean_price_ratio_raw(prices_array: nq.Float2D, params: Trend) -> nq.Float2D:
    mean_price_ST: nq.Float2D = nq.metrics.roll.get_mean(
        array=prices_array, length=params.short, min_length=params.short
    )
    mean_price_LT: nq.Float2D = nq.metrics.roll.get_mean(
        array=prices_array, length=params.long, min_length=params.long
    )

    return nq.metrics.roll.ratio_normalization(
        nominator=mean_price_ST, denominator=mean_price_LT
    )


def get_median_price_ratio_raw(prices_array: nq.Float2D, params: Trend) -> nq.Float2D:
    median_price_ST: nq.Float2D = nq.metrics.roll.get_median(
        array=prices_array, length=params.short, min_length=params.short
    )
    median_price_LT: nq.Float2D = nq.metrics.roll.get_median(
        array=prices_array, length=params.long, min_length=params.long
    )

    return nq.metrics.roll.ratio_normalization(
        nominator=median_price_ST, denominator=median_price_LT
    )


def get_central_price_ratio_raw(prices_array: nq.Float2D, params: Trend) -> nq.Float2D:
    central_price_ST: nq.Float2D = nq.metrics.roll.get_central_point(
        array=prices_array, length=params.short, min_length=params.short
    )
    central_price_LT: nq.Float2D = nq.metrics.roll.get_central_point(
        array=prices_array, length=params.long, min_length=params.long
    )

    return nq.metrics.roll.ratio_normalization(
        nominator=central_price_ST, denominator=central_price_LT
    )


def get_mean_rate_of_change_raw(
    log_returns_array: nq.Float2D, params: Trend
) -> nq.Float2D:
    mean_returns: nq.Float2D = nq.metrics.roll.get_mean(
        array=log_returns_array, length=params.short, min_length=params.short
    )

    return nq.metrics.roll.get_sum(
        array=mean_returns, length=params.long, min_length=params.long
    )


def get_median_rate_of_change_raw(
    log_returns_array: nq.Float2D, params: Trend
) -> nq.Float2D:
    median_returns: nq.Float2D = nq.metrics.roll.get_median(
        array=log_returns_array, length=params.short, min_length=params.short
    )

    return nq.metrics.roll.get_sum(
        array=median_returns, length=params.long, min_length=params.long
    )


def get_mean_price_macd_raw(
    prices_array: nq.Float2D, params: Acceleration
) -> nq.Float2D:
    mean_price_ratio_raw: nq.Float2D = get_mean_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    mean_price_ratio_raw_sma: nq.Float2D = nq.metrics.roll.get_mean(
        array=mean_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return mean_price_ratio_raw - mean_price_ratio_raw_sma


def get_median_price_macd_raw(
    prices_array: nq.Float2D, params: Acceleration
) -> nq.Float2D:
    median_price_ratio_raw: nq.Float2D = get_median_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    median_price_ratio_raw_sma: nq.Float2D = nq.metrics.roll.get_mean(
        array=median_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return median_price_ratio_raw - median_price_ratio_raw_sma


def get_central_price_macd_raw(
    prices_array: nq.Float2D, params: Acceleration
) -> nq.Float2D:
    central_price_ratio_raw: nq.Float2D = get_central_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    central_price_ratio_raw_sma: nq.Float2D = nq.metrics.roll.get_mean(
        array=central_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return central_price_ratio_raw - central_price_ratio_raw_sma


def get_mean_rate_of_change_macd_raw(
    returns_array: nq.Float2D, params: Acceleration
) -> nq.Float2D:
    mean_roc_raw: nq.Float2D = get_mean_rate_of_change_raw(
        log_returns_array=returns_array, params=params.trend
    )
    mean_roc_raw_sma: nq.Float2D = nq.metrics.roll.get_mean(
        array=mean_roc_raw, length=params.acceleration, min_length=params.acceleration
    )

    return mean_roc_raw - mean_roc_raw_sma


def get_median_rate_of_change_macd_raw(
    returns_array: nq.Float2D, params: Acceleration
) -> nq.Float2D:
    median_roc_raw: nq.Float2D = get_median_rate_of_change_raw(
        log_returns_array=returns_array, params=params.trend
    )
    median_roc_raw_sma: nq.Float2D = nq.metrics.roll.get_mean(
        array=median_roc_raw, length=params.acceleration, min_length=params.acceleration
    )
    return median_roc_raw - median_roc_raw_sma


def get_normalised_mean_price_ratio_raw(
    prices_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    mean_roc: nq.Float2D = nq.metrics.roll.relative_normalization(
        signal_array=prices_array, length=params.smoothing
    )
    return nq.metrics.roll.get_median_normalisation(
        signal_array=-mean_roc, window_length=params.signal
    )


def get_normalised_mean_rate_of_change_raw(
    log_returns_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    mean_roc: nq.Float2D = nq.metrics.roll.get_sum(
        array=log_returns_array, length=params.smoothing
    )
    return nq.metrics.roll.get_median_normalisation(
        signal_array=-mean_roc, window_length=params.signal
    )


def smoothed_skewness(
    log_returns_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    smoothed_array: nq.Float2D = nq.metrics.roll.get_mean(
        array=log_returns_array, length=params.smoothing, min_length=params.smoothing
    )
    return nq.metrics.roll.get_skewness(
        array=smoothed_array, length=params.signal, min_length=params.signal
    )


def smoothed_kurtosis(
    log_returns_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    smoothed_array: nq.Float2D = nq.metrics.roll.get_mean(
        array=log_returns_array, length=params.smoothing, min_length=params.smoothing
    )

    return nq.metrics.roll.get_kurtosis(
        array=smoothed_array, length=params.signal, min_length=params.signal
    )


def get_relative_skewness(
    log_returns_array: nq.Float2D, params: NormalizedSmoothedSignal
) -> nq.Float2D:
    skewness_array: nq.Float2D = smoothed_skewness(
        log_returns_array=log_returns_array,
        params=params.smoothed_signal,
    )
    return nq.metrics.roll.relative_normalization(
        signal_array=skewness_array, length=params.normalization
    )


def get_relative_kurt(
    log_returns_array: nq.Float2D, params: NormalizedSmoothedSignal
) -> nq.Float2D:
    kurtosis_array: nq.Float2D = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        params=params.smoothed_signal,
    )
    return nq.metrics.roll.relative_normalization(
        signal_array=kurtosis_array, length=params.normalization
    )


# TODO: trouver moyen de separer ces 2 strategies conditionnelles
def get_skew_on_kurtosis(
    log_returns_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    skew: nq.Float2D = smoothed_skewness(
        log_returns_array=log_returns_array,
        params=params,
    )
    kurt: nq.Float2D = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        params=params,
    )
    if params.signal <= 64:
        skew_on_kurt_signal: nq.Float2D = nq.metrics.roll.invert_signal_long(
            metric=kurt, signal=skew
        )
    else:
        skew_on_kurt_signal: nq.Float2D = nq.metrics.roll.invert_signal_short(
            metric=kurt, signal=skew
        )

    return skew_on_kurt_signal


def get_relative_skew_on_kurtosis(
    log_returns_array: nq.Float2D, params: NormalizedSmoothedSignal
) -> nq.Float2D:
    relative_skew: nq.Float2D = get_relative_skewness(
        log_returns_array=log_returns_array,
        params=params,
    )
    relative_kurt: nq.Float2D = get_relative_kurt(
        log_returns_array=log_returns_array,
        params=params,
    )
    if params.smoothed_signal.signal <= 64:
        relative_skew_on_kurt_signal: nq.Float2D = nq.metrics.roll.invert_signal_short(
            metric=relative_kurt, signal=relative_skew
        )
    else:
        relative_skew_on_kurt_signal: nq.Float2D = nq.metrics.roll.invert_signal_long(
            metric=relative_kurt, signal=relative_skew
        )

    return relative_skew_on_kurt_signal


def separate_volatility(
    array: nq.Float2D, len_vol: int
) -> tuple[nq.Float2D, nq.Float2D]:
    positive_returns: nq.Float2D = nq.metrics.roll.long_bias_normalization(
        signal_array=array
    )
    negative_returns: nq.Float2D = nq.metrics.roll.short_bias_normalization(
        signal_array=array
    )

    vol_positive: nq.Float2D = nq.metrics.roll.get_volatility(
        array=positive_returns, length=len_vol, min_length=1
    )
    vol_negative: nq.Float2D = nq.metrics.roll.get_volatility(
        array=negative_returns, length=len_vol, min_length=1
    )

    return vol_positive, vol_negative


def smoothed_directional_volatility(
    returns_array: nq.Float2D, params: SmoothedSignal
) -> nq.Float2D:
    smoothed_array: nq.Float2D = nq.metrics.roll.get_mean(
        array=returns_array, length=params.smoothing, min_length=params.smoothing
    )
    positive_vol, negative_vol = separate_volatility(
        array=smoothed_array, len_vol=params.signal
    )

    return positive_vol - negative_vol


def relative_directional_volatility(
    log_returns_array: nq.Float2D, params: Volatility
) -> nq.Float2D:
    directional_volatility_raw: nq.Float2D = smoothed_directional_volatility(
        returns_array=log_returns_array, params=params.smoothed_signal
    )
    return nq.metrics.roll.relative_normalization(
        signal_array=directional_volatility_raw, length=params.normalization
    )


def normalised_directional_volatility(
    log_returns_array: nq.Float2D, params: Volatility
) -> nq.Float2D:
    directional_volatility_raw: nq.Float2D = smoothed_directional_volatility(
        returns_array=log_returns_array,
        params=params.smoothed_signal,
    )
    return nq.metrics.roll.get_median_normalisation(
        signal_array=directional_volatility_raw, window_length=params.normalization
    )
