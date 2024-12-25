import numpy as np
from .Signals_Raw import *
from .Signals_Normalization import sign_normalization, calculate_indicator_on_trend_signal, rolling_median_normalisation, relative_normalization
from numpy.typing import NDArray

def mean_price_ratio(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    mean_price_ratio_raw = calculate_mean_price_ratio_raw(prices_array, LenST, LenLT)
    return sign_normalization(mean_price_ratio_raw)

def median_price_ratio(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    median_price_ratio_raw = calculate_median_price_ratio_raw(prices_array, LenST, LenLT)
    return sign_normalization(median_price_ratio_raw)

def central_price_ratio(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    central_price_ratio_raw = calculate_central_price_ratio_raw(prices_array, LenST, LenLT)
    return sign_normalization(central_price_ratio_raw)

def mean_rate_of_change(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    mean_roc_raw = calculate_mean_rate_of_change_raw(returns_array, LenST, LenLT)
    return sign_normalization(mean_roc_raw)

def median_rate_of_change(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    median_roc_raw = calculate_median_rate_of_change_raw(returns_array, LenST, LenLT)
    return sign_normalization(median_roc_raw)

def central_rate_of_change(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:
    central_roc_raw = calculate_central_rate_of_change_raw(returns_array, LenST, LenLT)
    return sign_normalization(central_roc_raw)

def mean_price_macd(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    mean_price_ratio_macd_raw = calculate_mean_price_macd_raw(prices_array, LenST, LenLT, MacdLength)
    return sign_normalization(mean_price_ratio_macd_raw)

def median_price_macd(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    median_price_ratio_macd_raw = calculate_median_price_macd_raw(prices_array, LenST, LenLT, MacdLength)
    return sign_normalization(median_price_ratio_macd_raw)

def central_price_macd(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    central_price_ratio_macd_raw = calculate_central_price_macd_raw(prices_array, LenST, LenLT, MacdLength)
    return sign_normalization(central_price_ratio_macd_raw)

def mean_rate_of_change_macd(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    mean_roc_macd_raw = calculate_mean_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)
    return sign_normalization(mean_roc_macd_raw)

def median_rate_of_change_macd(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    median_roc_macd_raw = calculate_median_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)
    return sign_normalization(median_roc_macd_raw)

def central_rate_of_change_macd(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:
    central_roc_macd_raw = calculate_central_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)
    return sign_normalization(central_roc_macd_raw)

def mean_price_macd_trend(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    mean_price_ratio_signal = mean_price_ratio(prices_array, TrendLenST, TrendLenLT)
    mean_price_macd_signal = mean_price_macd(prices_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(mean_price_ratio_signal, mean_price_macd_signal)

def median_price_macd_trend(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    median_price_ratio_signal = median_price_ratio(prices_array, TrendLenST, TrendLenLT)
    median_price_macd_signal = median_price_macd(prices_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(median_price_ratio_signal, median_price_macd_signal)

def central_price_macd_trend(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    central_price_ratio_signal = central_price_ratio(prices_array, TrendLenST, TrendLenLT)
    central_price_macd_signal = central_price_macd(prices_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(central_price_ratio_signal, central_price_macd_signal)

def mean_rate_of_change_macd_trend(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    mean_roc_trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    mean_roc_macd_signal = mean_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(mean_roc_trend_signal, mean_roc_macd_signal)

def median_rate_of_change_macd_trend(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    median_roc_trend_signal = median_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    median_roc_macd_signal = median_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(median_roc_trend_signal, median_roc_macd_signal)

def central_rate_of_change_macd_trend(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    central_roc_trend_signal = central_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    central_roc_macd_signal = central_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
    return calculate_indicator_on_trend_signal(central_roc_trend_signal, central_roc_macd_signal)

def fixed_bias(prices_array: NDArray[np.float32], Bias: int) -> NDArray[np.float32]:
    return np.full_like(prices_array, Bias, dtype=np.float32)

def mean_price_ratio_normalised(prices_array: NDArray[np.float32], SignalLength: int, PLength: int) -> NDArray[np.float32]:
    mean_price_ratio = calculate_mean_price_ratio_raw(prices_array, 1, SignalLength)
    return rolling_median_normalisation(-mean_price_ratio, PLength)

def mean_rate_of_change_normalised(returns_array: NDArray[np.float32], SignalLength: int, PLength: int) -> NDArray[np.float32]:
    mean_roc = calculate_mean_rate_of_change_raw(returns_array, 1, SignalLength)
    return rolling_median_normalisation(-mean_roc, PLength)

def mean_price_ratio_normalised_trend(prices_array: NDArray[np.float32], SignalLength: int, PLength: int, LenST: int, LenLT: int) -> NDArray[np.float32]:
    mean_reversion_signal = mean_price_ratio_normalised(prices_array, SignalLength, PLength)
    trend_signal = mean_price_ratio(prices_array, LenST, LenLT)
    return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)

def mean_rate_of_change_normalised_trend(returns_array: NDArray[np.float32], SignalLength: int, PLength: int, LenST: int, LenLT: int) -> NDArray[np.float32]:
    mean_reversion_signal = mean_rate_of_change_normalised(returns_array, SignalLength, PLength)
    trend_signal = mean_rate_of_change(returns_array, LenST, LenLT)
    return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)

def skewness(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    skewness_array = smoothed_skewness(returns_array, LenSmooth, LenSkew)
    return sign_normalization(-skewness_array)

def relative_skewness(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    skewness_array = smoothed_skewness(returns_array, LenSmooth, LenSkew)
    relative_skew = relative_normalization(skewness_array, LenSkew*4)
    return sign_normalization(relative_skew)

def skewness_on_kurtosis(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    skewness_array = smoothed_skewness(returns_array, LenSmooth, LenSkew)
    kurtosis_array = smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
    relative_kurt = relative_normalization(kurtosis_array, 2500)
    if LenSkew <= 64:
        skew_on_kurt_signal = np.where(relative_kurt < 0, -skewness_array, skewness_array)
    else:
        skew_on_kurt_signal = np.where(relative_kurt < 0, skewness_array, -skewness_array)
    return sign_normalization(skew_on_kurt_signal)

def relative_skewness_on_kurtosis(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    skewness_array = smoothed_skewness(returns_array, LenSmooth, LenSkew)
    kurtosis_array = smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
    relative_skew = relative_normalization(skewness_array, 2500)
    relative_kurt = relative_normalization(kurtosis_array, 2500)
    if LenSkew <= 64:
        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, -relative_skew, relative_skew)
    else:
        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, relative_skew, -relative_skew)
    return sign_normalization(relative_skew_on_kurt_signal)

def skewness_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    skewness_signal = skewness(returns_array, LenSmooth, LenSkew)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, skewness_signal)

def relative_skewness_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    relative_skewness_signal = relative_skewness(returns_array, LenSmooth, LenSkew)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, relative_skewness_signal)

def skewness_on_kurtosis_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    skew_on_kurt_signal = skewness_on_kurtosis(returns_array, LenSmooth, LenSkew)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)

def relative_skewness_on_kurtosis_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    relative_skew_on_kurt_signal = relative_skewness_on_kurtosis(returns_array, LenSmooth, LenSkew)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)

def relative_directional_volatility(returns_array: NDArray[np.float32], LenSmooth: int, LenRelative: int, LenVol: int) -> NDArray[np.float32]:
    directional_volatility_raw = smoothed_directional_volatility(returns_array, LenSmooth, LenVol)
    relative_directional_vol_raw = relative_normalization(directional_volatility_raw, LenRelative)
    return sign_normalization(relative_directional_vol_raw)

def normalised_directional_volatility(returns_array: NDArray[np.float32], LenSmooth: int, LenNormalization: int, LenVol: int) -> NDArray[np.float32]:
    directional_volatility_raw = smoothed_directional_volatility(returns_array, LenSmooth, LenVol)
    return rolling_median_normalisation(-directional_volatility_raw, LenNormalization)

def relative_directional_volatility_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenRelative: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    relative_directional_vol_signal = relative_directional_volatility(returns_array, LenSmooth, LenRelative, LenVol)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, relative_directional_vol_signal)

def normalised_directional_volatility_trend(returns_array: NDArray[np.float32], LenSmooth: int, LenNormalization: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> NDArray[np.float32]:
    normalised_directional_vol_signal = normalised_directional_volatility(returns_array, LenSmooth, LenNormalization, LenVol)
    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    return calculate_indicator_on_trend_signal(trend_signal, normalised_directional_vol_signal)
