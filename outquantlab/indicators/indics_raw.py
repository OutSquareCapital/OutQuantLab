import outquantlab.metrics as mt
from outquantlab.structures import arrays


def get_fixed_bias(prices_array: arrays.ArrayFloat, Bias: float) -> arrays.ArrayFloat:
    return arrays.full_array_like(model=prices_array, fill_value=Bias)


def get_mean_price_ratio_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    mean_price_ST: arrays.ArrayFloat = mt.get_rolling_mean(
        array=prices_array, length=len_st, min_length=len_st
    )
    mean_price_LT: arrays.ArrayFloat = mt.get_rolling_mean(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(nominator=mean_price_ST, denominator=mean_price_LT)


def get_median_price_ratio_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    median_price_ST: arrays.ArrayFloat = mt.get_rolling_median(
        array=prices_array, length=len_st, min_length=len_st
    )
    median_price_LT: arrays.ArrayFloat = mt.get_rolling_median(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(
        nominator=median_price_ST, denominator=median_price_LT
    )


def get_central_price_ratio_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    central_price_ST: arrays.ArrayFloat = mt.get_rolling_central(
        array=prices_array, length=len_st, min_length=len_st
    )
    central_price_LT: arrays.ArrayFloat = mt.get_rolling_central(
        array=prices_array, length=len_lt, min_length=len_lt
    )

    return mt.ratio_normalization(
        nominator=central_price_ST, denominator=central_price_LT
    )


def get_mean_rate_of_change_raw(
    log_returns_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    mean_returns: arrays.ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_st, min_length=len_st
    )

    return mt.get_rolling_sum(array=mean_returns, length=len_lt, min_length=len_lt)


def get_median_rate_of_change_raw(
    log_returns_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    median_returns: arrays.ArrayFloat = mt.get_rolling_median(
        array=log_returns_array, length=len_st, min_length=len_st
    )

    return mt.get_rolling_sum(array=median_returns, length=len_lt, min_length=len_lt)


def get_central_rate_of_change_raw(
    log_returns_array: arrays.ArrayFloat, len_st: int, len_lt: int
) -> arrays.ArrayFloat:
    central_returns: arrays.ArrayFloat = mt.get_rolling_quantile_ratio(
        returns_array=log_returns_array, window=len_st, quantile_spread=0.25
    )

    return mt.get_rolling_sum(array=central_returns, length=len_lt, min_length=len_lt)


def get_mean_price_macd_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    mean_price_ratio_raw: arrays.ArrayFloat = get_mean_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    mean_price_ratio_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        array=mean_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return mean_price_ratio_raw - mean_price_ratio_raw_sma


def get_median_price_macd_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    median_price_ratio_raw: arrays.ArrayFloat = get_median_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    median_price_ratio_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        median_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return median_price_ratio_raw - median_price_ratio_raw_sma


def get_central_price_macd_raw(
    prices_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    central_price_ratio_raw: arrays.ArrayFloat = get_central_price_ratio_raw(
        prices_array=prices_array, len_st=len_st, len_lt=len_lt
    )
    central_price_ratio_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        array=central_price_ratio_raw, length=len_macd, min_length=len_macd
    )

    return central_price_ratio_raw - central_price_ratio_raw_sma


def get_mean_rate_of_change_macd_raw(
    returns_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    mean_roc_raw: arrays.ArrayFloat = get_mean_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    mean_roc_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        array=mean_roc_raw, length=len_macd, min_length=len_macd
    )

    return mean_roc_raw - mean_roc_raw_sma


def get_median_rate_of_change_macd_raw(
    returns_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    median_roc_raw: arrays.ArrayFloat = get_median_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    median_roc_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        array=median_roc_raw, length=len_macd, min_length=len_macd
    )

    return median_roc_raw - median_roc_raw_sma


def get_central_rate_of_change_macd_raw(
    returns_array: arrays.ArrayFloat, len_st: int, len_lt: int, len_macd: int
) -> arrays.ArrayFloat:
    central_roc_raw: arrays.ArrayFloat = get_central_rate_of_change_raw(
        log_returns_array=returns_array, len_st=len_st, len_lt=len_lt
    )
    central_roc_raw_sma: arrays.ArrayFloat = mt.get_rolling_mean(
        array=central_roc_raw, length=len_macd, min_length=len_macd
    )

    return central_roc_raw - central_roc_raw_sma


def get_normalised_mean_price_ratio_raw(
    prices_array: arrays.ArrayFloat, len_signal: int, len_norm: int
) -> arrays.ArrayFloat:
    mean_roc: arrays.ArrayFloat = get_mean_price_ratio_raw(
        prices_array=prices_array, len_st=1, len_lt=len_signal
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=len_norm
    )


def get_normalised_mean_rate_of_change_raw(
    log_returns_array: arrays.ArrayFloat, len_signal: int, len_norm: int
) -> arrays.ArrayFloat:
    mean_roc: arrays.ArrayFloat = get_mean_rate_of_change_raw(
        log_returns_array=log_returns_array, len_st=1, len_lt=len_signal
    )
    return mt.get_rolling_median_normalisation(
        signal_array=-mean_roc, window_length=len_norm
    )


def smoothed_skewness(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    smoothed_array: arrays.ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_smooth, min_length=len_smooth
    )
    return mt.get_rolling_skewness(
        array=smoothed_array, length=len_skew, min_length=len_skew
    )


def smoothed_kurtosis(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    smoothed_array: arrays.ArrayFloat = mt.get_rolling_mean(
        array=log_returns_array, length=len_smooth, min_length=len_smooth
    )

    return mt.get_rolling_kurtosis(
        array=smoothed_array, length=len_skew, min_length=len_skew
    )


def get_relative_skewness(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    skewness_array: arrays.ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    return mt.relative_normalization(signal_array=skewness_array, length=len_skew * 4)


def get_relative_kurt(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    kurtosis_array: arrays.ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    return mt.relative_normalization(signal_array=kurtosis_array, length=2500)


def get_skew_on_kurtosis(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    skew: arrays.ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    kurt: arrays.ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    if len_skew <= 64:
        skew_on_kurt_signal: arrays.ArrayFloat = mt.dynamic_signal(
            metric=kurt, signal=skew
        )
    else:
        skew_on_kurt_signal: arrays.ArrayFloat = mt.dynamic_signal(
            metric=kurt, signal=-skew
        )

    return skew_on_kurt_signal


def get_relative_skew_on_kurtosis(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_skew: int
) -> arrays.ArrayFloat:
    relative_skew: arrays.ArrayFloat = get_relative_skewness(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    relative_kurt: arrays.ArrayFloat = get_relative_kurt(
        log_returns_array=log_returns_array,
        len_smooth=len_smooth,
        len_skew=len_skew,
    )
    if len_skew <= 64:
        relative_skew_on_kurt_signal: arrays.ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=-relative_skew
        )
    else:
        relative_skew_on_kurt_signal: arrays.ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=relative_skew
        )

    return relative_skew_on_kurt_signal


def smoothed_directional_volatility(
    returns_array: arrays.ArrayFloat, len_st: int, len_vol: int
) -> arrays.ArrayFloat:
    smoothed_array: arrays.ArrayFloat = mt.get_rolling_mean(
        array=returns_array, length=len_st, min_length=len_st
    )
    positive_vol, negative_vol = mt.separate_volatility(
        array=smoothed_array, len_vol=len_vol
    )

    return positive_vol - negative_vol


def relative_directional_volatility(
    log_returns_array: arrays.ArrayFloat,
    len_smooth: int,
    len_vol: int,
    len_relative: int,
) -> arrays.ArrayFloat:
    directional_volatility_raw: arrays.ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array, len_st=len_smooth, len_vol=len_vol
    )
    return mt.relative_normalization(
        signal_array=directional_volatility_raw, length=len_relative
    )


def normalised_directional_volatility(
    log_returns_array: arrays.ArrayFloat, len_smooth: int, len_vol: int, len_norm: int
) -> arrays.ArrayFloat:
    directional_volatility_raw: arrays.ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array,
        len_st=len_smooth,
        len_vol=len_vol,
    )
    return mt.get_rolling_median_normalisation(
        signal_array=directional_volatility_raw, window_length=len_norm
    )
