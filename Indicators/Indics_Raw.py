import Metrics as mt
from TypingConventions import ArrayFloat


def calculate_mean_price_ratio_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    mean_price_ST: ArrayFloat = mt.rolling_mean(
        array=prices_array, length=LenST, min_length=LenST
    )
    mean_price_LT: ArrayFloat = mt.rolling_mean(
        array=prices_array, length=LenLT, min_length=LenLT
    )

    return mt.ratio_normalization(nominator=mean_price_ST, denominator=mean_price_LT)


def calculate_median_price_ratio_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    median_price_ST: ArrayFloat = mt.rolling_median(
        array=prices_array, length=LenST, min_length=LenST
    )
    median_price_LT: ArrayFloat = mt.rolling_median(
        array=prices_array, length=LenLT, min_length=LenLT
    )

    return mt.ratio_normalization(
        nominator=median_price_ST, denominator=median_price_LT
    )


def calculate_central_price_ratio_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    central_price_ST: ArrayFloat = mt.rolling_central(
        array=prices_array, length=LenST, min_length=LenST
    )
    central_price_LT: ArrayFloat = mt.rolling_central(
        array=prices_array, length=LenLT, min_length=LenLT
    )

    return mt.ratio_normalization(
        nominator=central_price_ST, denominator=central_price_LT
    )


def calculate_mean_rate_of_change_raw(
    log_returns_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    mean_returns: ArrayFloat = mt.rolling_mean(
        array=log_returns_array, length=LenST, min_length=LenST
    )

    return mt.rolling_sum(array=mean_returns, length=LenLT, min_length=LenLT)


def calculate_median_rate_of_change_raw(
    log_returns_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    median_returns: ArrayFloat = mt.rolling_median(
        array=log_returns_array, length=LenST, min_length=LenST
    )

    return mt.rolling_sum(array=median_returns, length=LenLT, min_length=LenLT)


def calculate_central_rate_of_change_raw(
    log_returns_array: ArrayFloat, LenST: int, LenLT: int
) -> ArrayFloat:
    central_returns: ArrayFloat = mt.rolling_quantile_ratio(
        returns_array=log_returns_array, window=LenST, quantile_spread=0.25
    )

    return mt.rolling_sum(array=central_returns, length=LenLT, min_length=LenLT)


def calculate_mean_price_macd_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    mean_price_ratio_raw: ArrayFloat = calculate_mean_price_ratio_raw(
        prices_array=prices_array, LenST=LenST, LenLT=LenLT
    )
    mean_price_ratio_raw_sma: ArrayFloat = mt.rolling_mean(
        array=mean_price_ratio_raw, length=MacdLength, min_length=MacdLength
    )

    return mean_price_ratio_raw - mean_price_ratio_raw_sma


def calculate_median_price_macd_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    median_price_ratio_raw: ArrayFloat = calculate_median_price_ratio_raw(
        prices_array=prices_array, LenST=LenST, LenLT=LenLT
    )
    median_price_ratio_raw_sma: ArrayFloat = mt.rolling_mean(
        median_price_ratio_raw, length=MacdLength, min_length=MacdLength
    )

    return median_price_ratio_raw - median_price_ratio_raw_sma


def calculate_central_price_macd_raw(
    prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    central_price_ratio_raw: ArrayFloat = calculate_central_price_ratio_raw(
        prices_array=prices_array, LenST=LenST, LenLT=LenLT
    )
    central_price_ratio_raw_sma: ArrayFloat = mt.rolling_mean(
        array=central_price_ratio_raw, length=MacdLength, min_length=MacdLength
    )

    return central_price_ratio_raw - central_price_ratio_raw_sma


def calculate_mean_rate_of_change_macd_raw(
    returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    mean_roc_raw: ArrayFloat = calculate_mean_rate_of_change_raw(
        log_returns_array=returns_array, LenST=LenST, LenLT=LenLT
    )
    mean_roc_raw_sma: ArrayFloat = mt.rolling_mean(
        array=mean_roc_raw, length=MacdLength, min_length=MacdLength
    )

    return mean_roc_raw - mean_roc_raw_sma


def calculate_median_rate_of_change_macd_raw(
    returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    median_roc_raw: ArrayFloat = calculate_median_rate_of_change_raw(
        log_returns_array=returns_array, LenST=LenST, LenLT=LenLT
    )
    median_roc_raw_sma: ArrayFloat = mt.rolling_mean(
        array=median_roc_raw, length=MacdLength, min_length=MacdLength
    )

    return median_roc_raw - median_roc_raw_sma


def calculate_central_rate_of_change_macd_raw(
    returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int
) -> ArrayFloat:
    central_roc_raw: ArrayFloat = calculate_central_rate_of_change_raw(
        log_returns_array=returns_array, LenST=LenST, LenLT=LenLT
    )
    central_roc_raw_sma: ArrayFloat = mt.rolling_mean(
        array=central_roc_raw, length=MacdLength, min_length=MacdLength
    )

    return central_roc_raw - central_roc_raw_sma


def calculate_normalised_mean_price_ratio_raw(
    prices_array: ArrayFloat, SignalLength: int, PLength: int
) -> ArrayFloat:
    mean_roc: ArrayFloat = calculate_mean_price_ratio_raw(
        prices_array=prices_array, LenST=1, LenLT=SignalLength
    )
    return mt.rolling_median_normalisation(
        signal_array=-mean_roc, window_length=PLength
    )


def calculate_normalised_mean_rate_of_change_raw(
    log_returns_array: ArrayFloat, SignalLength: int, PLength: int
) -> ArrayFloat:
    mean_roc: ArrayFloat = calculate_mean_rate_of_change_raw(
        log_returns_array=log_returns_array, LenST=1, LenLT=SignalLength
    )
    return mt.rolling_median_normalisation(
        signal_array=-mean_roc, window_length=PLength
    )


def smoothed_skewness(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.rolling_mean(
        array=log_returns_array, length=LenSmooth, min_length=LenSmooth
    )
    return mt.rolling_skewness(array=smoothed_array, length=LenSkew, min_length=LenSkew)


def smoothed_kurtosis(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.rolling_mean(
        array=log_returns_array, length=LenSmooth, min_length=LenSmooth
    )

    return mt.rolling_kurtosis(array=smoothed_array, length=LenSkew, min_length=LenSkew)


def calculate_relative_skewness(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    skewness_array: ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    return mt.relative_normalization(signal_array=skewness_array, length=LenSkew * 4)


def calculate_relative_kurt(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    kurtosis_array: ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    return mt.relative_normalization(signal_array=kurtosis_array, length=2500)


def calculate_skew_on_kurtosis(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    skew: ArrayFloat = smoothed_skewness(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    kurt: ArrayFloat = smoothed_kurtosis(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    if LenSkew <= 64:
        skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(metric=kurt, signal=skew)
    else:
        skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(metric=kurt, signal=-skew)

    return skew_on_kurt_signal


def calculate_relative_skew_on_kurtosis(
    log_returns_array: ArrayFloat, LenSmooth: int, LenSkew: int
) -> ArrayFloat:
    relative_skew: ArrayFloat = calculate_relative_skewness(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    relative_kurt: ArrayFloat = calculate_relative_kurt(
        log_returns_array=log_returns_array,
        LenSmooth=LenSmooth,
        LenSkew=LenSkew,
    )
    if LenSkew <= 64:
        relative_skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=-relative_skew
        )
    else:
        relative_skew_on_kurt_signal: ArrayFloat = mt.dynamic_signal(
            metric=relative_kurt, signal=relative_skew
        )

    return relative_skew_on_kurt_signal


def smoothed_directional_volatility(
    returns_array: ArrayFloat, LenST: int, LenVol: int
) -> ArrayFloat:
    smoothed_array: ArrayFloat = mt.rolling_mean(
        array=returns_array, length=LenST, min_length=LenST
    )
    positive_vol, negative_vol = mt.separate_volatility(
        array=smoothed_array, LenVol=LenVol
    )

    return positive_vol - negative_vol


def relative_directional_volatility(
    log_returns_array: ArrayFloat, LenSmooth: int, LenVol: int, LenRelative: int
) -> ArrayFloat:
    directional_volatility_raw: ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array, LenST=LenSmooth, LenVol=LenVol
    )
    return mt.relative_normalization(
        signal_array=directional_volatility_raw, length=LenRelative
    )


def normalised_directional_volatility(
    log_returns_array: ArrayFloat, LenSmooth: int, LenVol: int, LenNormalization: int
) -> ArrayFloat:
    directional_volatility_raw: ArrayFloat = smoothed_directional_volatility(
        returns_array=log_returns_array,
        LenST=LenSmooth,
        LenVol=LenVol,
    )
    return mt.rolling_median_normalisation(
        signal_array=directional_volatility_raw, window_length=LenNormalization
    )
