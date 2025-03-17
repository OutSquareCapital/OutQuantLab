import outquantlab.metrics as mt
from outquantlab.typing_conventions import ArrayFloat, Float32
from numpy import full

def get_fixed_bias(prices_array: ArrayFloat, Bias: float) -> ArrayFloat:
    return full(prices_array.shape, Bias, dtype=Float32)
    
def get_mean_price_ratio_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    mean_price_ST: ArrayFloat = mt.get_rolling_mean(
        array=prices_array, length=len_st, min_length=len_st
    )
    mean_price_LT: ArrayFloat = mt.get_rolling_mean(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(nominator=mean_price_ST, denominator=mean_price_LT)


def get_median_price_ratio_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    median_price_ST: ArrayFloat = mt.get_rolling_median(
        array=prices_array, length=len_st, min_length=len_st
    )
    median_price_LT: ArrayFloat = mt.get_rolling_median(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(
        nominator=median_price_ST, denominator=median_price_LT
    )


def get_central_price_ratio_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    central_price_ST: ArrayFloat = mt.get_rolling_central(
        array=prices_array, length=len_st, min_length=len_st
    )
    central_price_LT: ArrayFloat = mt.get_rolling_central(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(
        nominator=central_price_ST, denominator=central_price_LT
    )


def get_mean_rate_of_change_raw(
    log_returns_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    mean_returns: ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_st, min_length=len_st
    )

    return mt.get_rolling_sum(array=mean_returns, length=len_lt, min_length=len_lt)


def get_median_rate_of_change_raw(
    log_returns_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    median_returns: ArrayFloat = mt.get_rolling_median(
        array=log_returns_array, length=len_st, min_length=len_st
    )

    return mt.get_rolling_sum(array=median_returns, length=len_lt, min_length=len_lt)


def get_central_rate_of_change_raw(
    log_returns_array: ArrayFloat, len_st: int, len_lt: int
) -> ArrayFloat:
    central_returns: ArrayFloat = mt.get_rolling_quantile_ratio(
        returns_array=log_returns_array, window=len_st, quantile_spread=0.25
    )

    return mt.get_rolling_sum(array=central_returns, length=len_lt, min_length=len_lt)


def get_mean_price_macd_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    mean_price_ratio_raw: ArrayFloat = get_mean_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    mean_price_ratio_raw_sma: ArrayFloat = mt.get_rolling_mean(
        array=mean_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return mean_price_ratio_raw - mean_price_ratio_raw_sma


def get_median_price_macd_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    median_price_ratio_raw: ArrayFloat = get_median_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    median_price_ratio_raw_sma: ArrayFloat = mt.get_rolling_mean(
        median_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return median_price_ratio_raw - median_price_ratio_raw_sma


def get_central_price_macd_raw(
    prices_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    central_price_ratio_raw: ArrayFloat = get_central_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    central_price_ratio_raw_sma: ArrayFloat = mt.get_rolling_mean(
        array=central_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return central_price_ratio_raw - central_price_ratio_raw_sma


def get_mean_rate_of_change_macd_raw(
    returns_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    mean_roc_raw: ArrayFloat = get_mean_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    mean_roc_raw_sma: ArrayFloat = mt.get_rolling_mean(
        array=mean_roc_raw, length=len_macd, min_length=len_macd
    )

    return mean_roc_raw - mean_roc_raw_sma


def get_median_rate_of_change_macd_raw(
    returns_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    median_roc_raw: ArrayFloat = get_median_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    median_roc_raw_sma: ArrayFloat = mt.get_rolling_mean(
        array=median_roc_raw, length=len_macd, min_length=len_macd
    )

    return median_roc_raw - median_roc_raw_sma


def get_central_rate_of_change_macd_raw(
    returns_array: ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> ArrayFloat:
    central_roc_raw: ArrayFloat = get_central_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    central_roc_raw_sma: ArrayFloat = mt.get_rolling_mean(
        array=central_roc_raw, length=len_macd, min_length=len_macd
    )

    return central_roc_raw - central_roc_raw_sma


def get_normalised_mean_price_ratio_raw(
    prices_array: ArrayFloat, len_signal: int, len_norm: int
) -> ArrayFloat:
    mean_roc: ArrayFloat = get_mean_price_ratio_raw(
        prices_array=prices_array, len_st=1, len_lt=len_signal
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=len_norm
    )


def get_normalised_mean_rate_of_change_raw(
    log_returns_array: ArrayFloat, len_signal: int, len_norm: int
) -> ArrayFloat:
    mean_roc: ArrayFloat = get_mean_rate_of_change_raw(
        log_returns_array=log_returns_array, len_st=1, len_lt=len_signal
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=len_norm
    )


def smoothed_skewness(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_smooth, min_length=len_smooth
    )
    return mt.rolling_skewness(
        array=smoothed_array, length=len_skew, min_length=len_skew
    )


def smoothed_kurtosis(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_smooth, min_length=len_smooth
    )

    return mt.rolling_kurtosis(
        array=smoothed_array, length=len_skew, min_length=len_skew
    )


def get_relative_skewness(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    skewness_array: ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    return mt.relative_normalization(signal_array=skewness_array, length=len_skew * 4)


def get_relative_kurt(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    kurtosis_array: ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    return mt.relative_normalization(signal_array=kurtosis_array, length=2500)


def get_skew_on_kurtosis(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    skew: ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    kurt: ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    if len_skew <= 64:
        skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(metric=kurt, signal=skew)
    else:
        skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(metric=kurt, signal=-skew)

    return skew_on_kurt_signal


def get_relative_skew_on_kurtosis(
    log_returns_array: ArrayFloat, len_smooth: int, len_skew: int
) -> ArrayFloat:
    relative_skew: ArrayFloat = get_relative_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    relative_kurt: ArrayFloat = get_relative_kurt(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    if len_skew <= 64:
        relative_skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=-relative_skew
        )
    else:
        relative_skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=relative_skew
        )

    return relative_skew_on_kurt_signal


def smoothed_directional_volatility(
    returns_array: ArrayFloat, len_st: int, len_vol: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.get_rolling_mean(
        array=returns_array, length=len_st, min_length=len_st
    )
    positive_vol, negative_vol = mt.separate_volatility(
        array=smoothed_array, len_vol=len_vol
    )

    return positive_vol - negative_vol


def relative_directional_volatility(
    log_returns_array: ArrayFloat, len_smooth: int, len_vol: int, len_relative: int
) -> ArrayFloat:
    directional_volatility_raw: ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array, len_st=len_smooth, len_vol=len_vol
    )
    return mt.relative_normalization(
        signal_array=directional_volatility_raw, length=len_relative
    )


def normalised_directional_volatility(
    log_returns_array: ArrayFloat, len_smooth: int, len_vol: int, len_norm: int
) -> ArrayFloat:
    directional_volatility_raw: ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array,
        len_st=len_smooth,
        len_vol=len_vol,
    )
    return mt.get_rolling_median_normalisation(
        signal_array=directional_volatility_raw, window_length=len_norm
    )
