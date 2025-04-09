import outquantlab.metrics as mt
from outquantlab.indicators.params_types import (
    Acceleration,
    SmoothedSignal,
    Trend,
    Volatility,
)
from outquantlab.structures import arrays


def get_mean_price_ratio_raw(
    prices_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    mean_price_ST: arrays.Float2D = mt.get_rolling_mean(
        array=prices_array, length=params.short, min_length=params.short
    )
    mean_price_LT: arrays.Float2D = mt.get_rolling_mean(
        array=prices_array, length=params.long, min_length=params.long
    )

    return mt.ratio_normalization(nominator=mean_price_ST, denominator=mean_price_LT)


def get_median_price_ratio_raw(
    prices_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    median_price_ST: arrays.Float2D = mt.get_rolling_median(
        array=prices_array, length=params.short, min_length=params.short
    )
    median_price_LT: arrays.Float2D = mt.get_rolling_median(
        array=prices_array, length=params.long, min_length=params.long
    )

    return mt.ratio_normalization(
        nominator=median_price_ST, denominator=median_price_LT
    )


def get_central_price_ratio_raw(
    prices_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    central_price_ST: arrays.Float2D = mt.get_rolling_central(
        array=prices_array, length=params.short, min_length=params.short
    )
    central_price_LT: arrays.Float2D = mt.get_rolling_central(
        array=prices_array, length=params.long, min_length=params.long
    )

    return mt.ratio_normalization(
        nominator=central_price_ST, denominator=central_price_LT
    )


def get_mean_rate_of_change_raw(
    log_returns_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    mean_returns: arrays.Float2D = mt.get_rolling_mean(
        array=log_returns_array, length=params.short, min_length=params.short
    )

    return mt.get_rolling_sum(
        array=mean_returns, length=params.long, min_length=params.long
    )


def get_median_rate_of_change_raw(
    log_returns_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    median_returns: arrays.Float2D = mt.get_rolling_median(
        array=log_returns_array, length=params.short, min_length=params.short
    )

    return mt.get_rolling_sum(
        array=median_returns, length=params.long, min_length=params.long
    )


def get_central_rate_of_change_raw(
    log_returns_array: arrays.Float2D, params: Trend
) -> arrays.Float2D:
    central_returns: arrays.Float2D = mt.get_rolling_quantile_ratio(
        returns_array=log_returns_array, window=params.short, quantile_spread=0.25
    )

    return mt.get_rolling_sum(
        array=central_returns, length=params.long, min_length=params.long
    )


def get_mean_price_macd_raw(
    prices_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    mean_price_ratio_raw: arrays.Float2D = get_mean_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    mean_price_ratio_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=mean_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return mean_price_ratio_raw - mean_price_ratio_raw_sma


def get_median_price_macd_raw(
    prices_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    median_price_ratio_raw: arrays.Float2D = get_median_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    median_price_ratio_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=median_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return median_price_ratio_raw - median_price_ratio_raw_sma


def get_central_price_macd_raw(
    prices_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    central_price_ratio_raw: arrays.Float2D = get_central_price_ratio_raw(
        prices_array=prices_array, params=params.trend
    )
    central_price_ratio_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=central_price_ratio_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return central_price_ratio_raw - central_price_ratio_raw_sma


def get_mean_rate_of_change_macd_raw(
    returns_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    mean_roc_raw: arrays.Float2D = get_mean_rate_of_change_raw(
        log_returns_array=returns_array, params=params.trend
    )
    mean_roc_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=mean_roc_raw, length=params.acceleration, min_length=params.acceleration
    )

    return mean_roc_raw - mean_roc_raw_sma


def get_median_rate_of_change_macd_raw(
    returns_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    median_roc_raw: arrays.Float2D = get_median_rate_of_change_raw(
        log_returns_array=returns_array, params=params.trend
    )
    median_roc_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=median_roc_raw, length=params.acceleration, min_length=params.acceleration
    )
    return median_roc_raw - median_roc_raw_sma


def get_central_rate_of_change_macd_raw(
    returns_array: arrays.Float2D, params: Acceleration
) -> arrays.Float2D:
    central_roc_raw: arrays.Float2D = get_central_rate_of_change_raw(
        log_returns_array=returns_array, params=params.trend
    )
    central_roc_raw_sma: arrays.Float2D = mt.get_rolling_mean(
        array=central_roc_raw,
        length=params.acceleration,
        min_length=params.acceleration,
    )

    return central_roc_raw - central_roc_raw_sma


def get_normalised_mean_price_ratio_raw(
    prices_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    mean_roc: arrays.Float2D = mt.relative_normalization(
        signal_array=prices_array, length=params.smoothing
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=params.signal
    )


def get_normalised_mean_rate_of_change_raw(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    mean_roc: arrays.Float2D = mt.get_rolling_sum(
        array=log_returns_array, length=params.smoothing
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=params.signal
    )


def smoothed_skewness(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    smoothed_array: arrays.Float2D = mt.get_rolling_mean(
        array=log_returns_array, length=params.smoothing, min_length=params.smoothing
    )
    return mt.get_rolling_skewness(
        array=smoothed_array, length=params.signal, min_length=params.signal
    )


def smoothed_kurtosis(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    smoothed_array: arrays.Float2D = mt.get_rolling_mean(
        array=log_returns_array, length=params.smoothing, min_length=params.smoothing
    )

    return mt.get_rolling_kurtosis(
        array=smoothed_array, length=params.signal, min_length=params.signal
    )


def get_relative_skewness(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    skewness_array: arrays.Float2D = smoothed_skewness(
        log_returns_array=log_returns_array,
        params=params,
    )
    return mt.relative_normalization(
        signal_array=skewness_array, length=params.signal * 4
    )


def get_relative_kurt(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    kurtosis_array: arrays.Float2D = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        params=params,
    )
    return mt.relative_normalization(signal_array=kurtosis_array, length=2500)


def get_skew_on_kurtosis(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    skew: arrays.Float2D = smoothed_skewness(
        log_returns_array=log_returns_array,
        params=params,
    )
    kurt: arrays.Float2D = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        params=params,
    )
    if params.signal <= 64:
        skew_on_kurt_signal: arrays.Float2D = mt.dynamic_signal(
            metric=kurt, signal=skew
        )
    else:
        skew_on_kurt_signal: arrays.Float2D = mt.dynamic_signal(
            metric=kurt, signal=-skew
        )

    return skew_on_kurt_signal


def get_relative_skew_on_kurtosis(
    log_returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    relative_skew: arrays.Float2D = get_relative_skewness(
        log_returns_array=log_returns_array,
        params=params,
    )
    relative_kurt: arrays.Float2D = get_relative_kurt(
        log_returns_array=log_returns_array,
        params=params,
    )
    if params.signal <= 64:
        relative_skew_on_kurt_signal: arrays.Float2D = mt.dynamic_signal(
            metric=relative_kurt, signal=-relative_skew
        )
    else:
        relative_skew_on_kurt_signal: arrays.Float2D = mt.dynamic_signal(
            metric=relative_kurt, signal=relative_skew
        )

    return relative_skew_on_kurt_signal


def smoothed_directional_volatility(
    returns_array: arrays.Float2D, params: SmoothedSignal
) -> arrays.Float2D:
    smoothed_array: arrays.Float2D = mt.get_rolling_mean(
        array=returns_array, length=params.smoothing, min_length=params.smoothing
    )
    positive_vol, negative_vol = mt.separate_volatility(
        array=smoothed_array, len_vol=params.signal
    )

    return positive_vol - negative_vol


def relative_directional_volatility(
    log_returns_array: arrays.Float2D, params: Volatility
) -> arrays.Float2D:
    directional_volatility_raw: arrays.Float2D = smoothed_directional_volatility(
        returns_array=log_returns_array, params=params.smoothed_signal
    )
    return mt.relative_normalization(
        signal_array=directional_volatility_raw, length=params.normalization
    )


def normalised_directional_volatility(
    log_returns_array: arrays.Float2D, params: Volatility
) -> arrays.Float2D:
    directional_volatility_raw: arrays.Float2D = smoothed_directional_volatility(
        returns_array=log_returns_array,
        params=params.smoothed_signal,
    )
    return mt.get_rolling_median_normalisation(
        signal_array=directional_volatility_raw, window_length=params.normalization
    )
