import numpy as np
import Metrics as mt
from .Signals_Normalization import ratio_normalization
from numpy.typing import NDArray

def generate_seasonal_array(returns_df) -> NDArray:

    def assign_week_of_month(day: int) -> int:
        if day <= 6:
            return 1
        elif day <= 12:
            return 2
        elif day <= 18:
            return 3
        else:
            return 4

    seasonal_array = np.empty((returns_df.shape[0], 3), dtype=np.int32)
    
    seasonal_array[:, 2] = returns_df.index.quarter

    day_of_month = returns_df.groupby([returns_df.index.year, returns_df.index.month], observed=False).cumcount() + 1
    seasonal_array[:, 1] = day_of_month.apply(assign_week_of_month).values

    seasonal_array[:, 0] = returns_df.index.dayofweek + 1

    return seasonal_array


def calculate_mean_price_ratio_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    mean_price_ST = mt.rolling_mean(prices_array, length=LenST, min_length=LenST)
    mean_price_LT = mt.rolling_mean(prices_array, length=LenLT, min_length=LenLT)

    return ratio_normalization(mean_price_ST, mean_price_LT)


def calculate_median_price_ratio_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    median_price_ST = mt.rolling_median(prices_array, length=LenST, min_length=LenST)
    median_price_LT = mt.rolling_median(prices_array, length=LenLT, min_length=LenLT)
    
    return ratio_normalization(median_price_ST, median_price_LT)


def calculate_central_price_ratio_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    central_price_ST = mt.rolling_central(prices_array, LenST, min_length=LenST)
    central_price_LT = mt.rolling_central(prices_array, LenLT, min_length=LenLT)

    return ratio_normalization(central_price_ST, central_price_LT)


def calculate_mean_rate_of_change_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    mean_returns = mt.rolling_mean(returns_array, length=LenST, min_length=LenST)

    return mt.rolling_sum(mean_returns, length=LenLT, min_length=LenLT)


def calculate_median_rate_of_change_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    median_returns = mt.rolling_median(returns_array, length=LenST, min_length=LenST)

    return mt.rolling_sum(median_returns, length=LenLT, min_length=LenLT)


def calculate_central_rate_of_change_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int) -> NDArray[np.float32]:

    central_returns = mt.rolling_quantile_ratio(returns_array=returns_array, window=LenST, quantile_spread=0.25)

    return mt.rolling_sum(central_returns, length=LenLT, min_length=LenLT)


def calculate_mean_price_macd_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    mean_price_ratio_raw = calculate_mean_price_ratio_raw(prices_array, LenST, LenLT)

    mean_price_ratio_raw_sma = mt.rolling_mean(mean_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (mean_price_ratio_raw - mean_price_ratio_raw_sma)


def calculate_median_price_macd_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    median_price_ratio_raw = calculate_median_price_ratio_raw(prices_array, LenST, LenLT)

    median_price_ratio_raw_sma = mt.rolling_mean(median_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (median_price_ratio_raw - median_price_ratio_raw_sma)


def calculate_central_price_macd_raw(prices_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    central_price_ratio_raw = calculate_central_price_ratio_raw(prices_array, LenST, LenLT)

    central_price_ratio_raw_sma = mt.rolling_mean(central_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (central_price_ratio_raw - central_price_ratio_raw_sma)


def calculate_mean_rate_of_change_macd_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    mean_roc_raw = calculate_mean_rate_of_change_raw(returns_array, LenST, LenLT)

    mean_roc_raw_sma = mt.rolling_mean(mean_roc_raw, length=MacdLength, min_length=MacdLength)

    return (mean_roc_raw - mean_roc_raw_sma)


def calculate_median_rate_of_change_macd_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    median_roc_raw = calculate_median_rate_of_change_raw(returns_array, LenST, LenLT)

    median_roc_raw_sma = mt.rolling_mean(median_roc_raw, length=MacdLength, min_length=MacdLength)

    return (median_roc_raw - median_roc_raw_sma)


def calculate_central_rate_of_change_macd_raw(returns_array: NDArray[np.float32], LenST: int, LenLT: int, MacdLength: int) -> NDArray[np.float32]:

    central_roc_raw = calculate_central_rate_of_change_raw(returns_array, LenST, LenLT)

    central_roc_raw_sma = mt.rolling_mean(central_roc_raw, length=MacdLength, min_length=MacdLength)

    return (central_roc_raw - central_roc_raw_sma)


def smoothed_skewness(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    
    smoothed_array = mt.rolling_mean(returns_array, length=LenSmooth, min_length=LenSmooth)

    return mt.rolling_skewness(smoothed_array, length=LenSkew, min_length=LenSkew)


def smoothed_kurtosis(returns_array: NDArray[np.float32], LenSmooth: int, LenSkew: int) -> NDArray[np.float32]:
    
    smoothed_array = mt.rolling_mean(returns_array, length=LenSmooth, min_length=LenSmooth)

    return mt.rolling_kurtosis(smoothed_array, length=LenSkew, min_length=LenSkew)


def smoothed_directional_volatility(returns_array: NDArray[np.float32], LenST: int, LenVol: int) -> NDArray[np.float32]:

    smoothed_array = mt.rolling_mean(returns_array, length=LenST, min_length=LenST)

    positive_vol, negative_vol = mt.separate_volatility(smoothed_array, LenVol)

    return (positive_vol - negative_vol)