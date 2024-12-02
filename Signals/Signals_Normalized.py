import numpy as np
from Signals.Signals_Raw import *
import Signals.Signals_Normalization as sn


def mean_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

    mean_price_ratio_raw = RawTrend.calculate_mean_price_ratio_raw(prices_array, LenST, LenLT)

    return sn.sign_normalization(mean_price_ratio_raw)


def median_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:
    
    median_price_ratio_raw = RawTrend.calculate_median_price_ratio_raw(prices_array, LenST, LenLT)

    return sn.sign_normalization(median_price_ratio_raw)


def central_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

    central_price_ratio_raw = RawTrend.calculate_central_price_ratio_raw(prices_array, LenST, LenLT)

    return sn.sign_normalization(central_price_ratio_raw)


def mean_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

    mean_roc_raw = RawTrend.calculate_mean_rate_of_change_raw(returns_array, LenST, LenLT)
    
    return sn.sign_normalization(mean_roc_raw)


def median_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

    median_roc_raw = RawTrend.calculate_median_rate_of_change_raw(returns_array, LenST, LenLT)

    return sn.sign_normalization(median_roc_raw)



def central_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

    central_roc_raw = RawTrend.calculate_central_rate_of_change_raw(returns_array, LenST, LenLT)

    return sn.sign_normalization(central_roc_raw)



def mean_price_macd(prices_array: np.ndarray, LenST: int, LenLT: int, MacdLength: int) -> np.ndarray:

    mean_price_ratio_macd_raw = RawAcceleration.calculate_mean_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(mean_price_ratio_macd_raw)


def median_price_macd(prices_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

    median_price_ratio_macd_raw = RawAcceleration.calculate_median_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(median_price_ratio_macd_raw)


def central_price_macd(prices_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

    central_price_ratio_macd_raw = RawAcceleration.calculate_central_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(central_price_ratio_macd_raw)


def mean_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

    mean_roc_macd_raw = RawAcceleration.calculate_mean_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(mean_roc_macd_raw)


def median_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

    median_roc_macd_raw = RawAcceleration.calculate_median_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(median_roc_macd_raw)


def central_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

    central_roc_macd_raw = RawAcceleration.calculate_central_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

    return sn.sign_normalization(central_roc_macd_raw)



def mean_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    mean_price_ratio_signal = mean_price_ratio(prices_array, TrendLenST, TrendLenLT)

    mean_price_macd_signal =  mean_price_macd(prices_array, LenST, LenLT, MacdLength)

    return sn.calculate_indicator_on_trend_signal(mean_price_ratio_signal, mean_price_macd_signal)


def median_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    median_price_ratio_signal = median_price_ratio(prices_array, TrendLenST, TrendLenLT)

    median_price_macd_signal = median_price_macd(prices_array, LenST, LenLT, MacdLength)
    
    return sn.calculate_indicator_on_trend_signal(median_price_ratio_signal, median_price_macd_signal)


def central_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    central_price_ratio_signal = central_price_ratio(prices_array, TrendLenST, TrendLenLT)

    central_price_macd_signal = central_price_macd(prices_array, LenST, LenLT, MacdLength)

    return sn.calculate_indicator_on_trend_signal(central_price_ratio_signal, central_price_macd_signal)


def mean_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    mean_roc_trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    mean_roc_macd_signal = mean_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
    
    return sn.calculate_indicator_on_trend_signal(mean_roc_trend_signal, mean_roc_macd_signal)


def median_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    median_roc_trend_signal = median_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    median_roc_macd_signal = median_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)

    return sn.calculate_indicator_on_trend_signal(median_roc_trend_signal, median_roc_macd_signal)


def central_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    central_roc_trend_signal = central_rate_of_change(returns_array, TrendLenST, TrendLenLT)
    
    central_roc_macd_signal = central_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
    
    return sn.calculate_indicator_on_trend_signal(central_roc_trend_signal, central_roc_macd_signal)



def fixed_bias(prices_array:np.ndarray, Bias:int) -> np.ndarray:

    return np.full_like(prices_array, Bias, dtype=np.float32)



def mean_price_ratio_normalised(prices_array:np.ndarray, SignalLength: int, PLength: int) -> np.ndarray:

    mean_price_ratio = RawTrend.calculate_mean_price_ratio_raw(prices_array, 1, SignalLength)

    return sn.rolling_median_normalisation(-mean_price_ratio, PLength)


def mean_rate_of_change_normalised(returns_array:np.ndarray, SignalLength: int, PLength: int) -> np.ndarray:

    mean_roc = RawTrend.calculate_mean_rate_of_change_raw(returns_array, 1, SignalLength)

    return sn.rolling_median_normalisation(-mean_roc, PLength)



def mean_price_ratio_normalised_trend(prices_array: np.ndarray, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> np.ndarray:

    mean_reversion_signal = mean_price_ratio_normalised(prices_array, SignalLength, PLength)

    trend_signal = mean_price_ratio(prices_array, LenST, LenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)


def mean_rate_of_change_normalised_trend(returns_array: np.ndarray, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> np.ndarray:

    mean_reversion_signal = mean_rate_of_change_normalised(returns_array, SignalLength, PLength)

    trend_signal = mean_rate_of_change(returns_array, LenST, LenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal) 



def skewness(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

    skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
    
    return sn.sign_normalization(-skewness_array)


def relative_skewness(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:
    
    skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)

    relative_skew = sn.relative_normalization(skewness_array, LenSkew*4)

    return sn.sign_normalization(relative_skew)


def skewness_on_kurtosis(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

    skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
    kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
    
    relative_kurt = sn.relative_normalization(kurtosis_array, 2500)

    if LenSkew <= 64:
        skew_on_kurt_signal = np.where(relative_kurt < 0, -skewness_array, skewness_array)
    else:
        skew_on_kurt_signal = np.where(relative_kurt < 0, skewness_array, -skewness_array)

    return sn.sign_normalization(skew_on_kurt_signal)

def relative_skewness_on_kurtosis(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

    skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
    kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
    
    relative_skew = sn.relative_normalization(skewness_array, 2500)
    relative_kurt = sn.relative_normalization(kurtosis_array, 2500)
    if LenSkew <= 64:
        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, -relative_skew, relative_skew)
    else:
        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, relative_skew, -relative_skew)

    return sn.sign_normalization(relative_skew_on_kurt_signal)

def skewness_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    skewness_signal = skewness(returns_array, LenSmooth, LenSkew)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, skewness_signal)


def relative_skewness_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    relative_skewness_signal = relative_skewness(returns_array, LenSmooth, LenSkew)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, relative_skewness_signal)


def skewness_on_kurtosis_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    skew_on_kurt_signal = skewness_on_kurtosis(returns_array, LenSmooth, LenSkew)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)


def relative_skewness_on_kurtosis_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    relative_skew_on_kurt_signal = relative_skewness_on_kurtosis(returns_array, LenSmooth, LenSkew)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)



def relative_directional_volatility(returns_array:np.ndarray, LenST:int, LenLT:int, LenVol: int) -> np.ndarray:

    directional_volatility_raw = RawVolatility.smoothed_directional_volatility(returns_array, LenST, LenVol)

    relative_directional_vol_raw = sn.relative_normalization(directional_volatility_raw, LenLT)

    return sn.sign_normalization(relative_directional_vol_raw)


def normalised_directional_volatility(returns_array:np.ndarray, LenST:int, LenLT:int, LenVol: int) -> np.ndarray:

    directional_volatility_raw = RawVolatility.smoothed_directional_volatility(returns_array, LenST, LenVol)

    return sn.rolling_median_normalisation(-directional_volatility_raw, LenLT*8)



def relative_directional_volatility_trend(returns_array: np.ndarray, LenST:int, LenLT:int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    relative_directional_vol_signal = relative_directional_volatility(returns_array, LenST,LenLT, LenVol)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, relative_directional_vol_signal)


def normalised_directional_volatility_trend(returns_array: np.ndarray, LenST:int, LenLT:int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

    normalised_directional_vol_signal = normalised_directional_volatility(returns_array, LenST,LenLT, LenVol)

    trend_signal = mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    return sn.calculate_indicator_on_trend_signal(trend_signal, normalised_directional_vol_signal)