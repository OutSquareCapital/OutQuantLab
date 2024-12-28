import numpy as np
from Metrics import (
rolling_mean, 
rolling_median, 
rolling_central,
rolling_sum,
rolling_quantile_ratio,
rolling_skewness,
rolling_kurtosis,
separate_volatility
)
from .Indics_Normalization import ratio_normalization
from Files import ArrayFloat, ArrayInt, DataFrameFloat, Int32

def generate_seasonal_array(returns_df: DataFrameFloat) -> ArrayInt:

    def assign_week_of_month(day: int) -> int:
        if day <= 6:
            return 1
        elif day <= 12:
            return 2
        elif day <= 18:
            return 3
        else:
            return 4

    seasonal_array = np.empty((returns_df.shape[0], 3), dtype=Int32)
    
    seasonal_array[:, 2] = returns_df.index.quarter

    day_of_month = returns_df.groupby([returns_df.index.year, returns_df.index.month], observed=False).cumcount() + 1 # type: ignore
    seasonal_array[:, 1] = day_of_month.apply(assign_week_of_month).to_numpy() # type: ignore

    seasonal_array[:, 0] = returns_df.index.dayofweek + 1

    return seasonal_array

def calculate_mean_price_ratio_raw(prices_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    mean_price_ST = rolling_mean(prices_array, length=LenST, min_length=LenST)
    mean_price_LT = rolling_mean(prices_array, length=LenLT, min_length=LenLT)

    return ratio_normalization(mean_price_ST, mean_price_LT)

def calculate_median_price_ratio_raw(prices_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    median_price_ST = rolling_median(prices_array, length=LenST, min_length=LenST)
    median_price_LT = rolling_median(prices_array, length=LenLT, min_length=LenLT)
    
    return ratio_normalization(median_price_ST, median_price_LT)

def calculate_central_price_ratio_raw(prices_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    central_price_ST = rolling_central(prices_array, LenST, min_length=LenST)
    central_price_LT = rolling_central(prices_array, LenLT, min_length=LenLT)

    return ratio_normalization(central_price_ST, central_price_LT)

def calculate_mean_rate_of_change_raw(returns_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    mean_returns = rolling_mean(returns_array, length=LenST, min_length=LenST)

    return rolling_sum(mean_returns, length=LenLT, min_length=LenLT)

def calculate_median_rate_of_change_raw(returns_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    median_returns = rolling_median(returns_array, length=LenST, min_length=LenST)

    return rolling_sum(median_returns, length=LenLT, min_length=LenLT)

def calculate_central_rate_of_change_raw(returns_array: ArrayFloat, LenST: int, LenLT: int) -> ArrayFloat:
    central_returns = rolling_quantile_ratio(returns_array=returns_array, window=LenST, quantile_spread=0.25)

    return rolling_sum(central_returns, length=LenLT, min_length=LenLT)

def calculate_mean_price_macd_raw(prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    mean_price_ratio_raw = calculate_mean_price_ratio_raw(prices_array, LenST, LenLT)
    mean_price_ratio_raw_sma = rolling_mean(mean_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (mean_price_ratio_raw - mean_price_ratio_raw_sma)


def calculate_median_price_macd_raw(prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    median_price_ratio_raw = calculate_median_price_ratio_raw(prices_array, LenST, LenLT)
    median_price_ratio_raw_sma = rolling_mean(median_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (median_price_ratio_raw - median_price_ratio_raw_sma)


def calculate_central_price_macd_raw(prices_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    central_price_ratio_raw = calculate_central_price_ratio_raw(prices_array, LenST, LenLT)
    central_price_ratio_raw_sma = rolling_mean(central_price_ratio_raw, length=MacdLength, min_length=MacdLength)

    return (central_price_ratio_raw - central_price_ratio_raw_sma)


def calculate_mean_rate_of_change_macd_raw(returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    mean_roc_raw = calculate_mean_rate_of_change_raw(returns_array, LenST, LenLT)
    mean_roc_raw_sma = rolling_mean(mean_roc_raw, length=MacdLength, min_length=MacdLength)

    return (mean_roc_raw - mean_roc_raw_sma)


def calculate_median_rate_of_change_macd_raw(returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    median_roc_raw = calculate_median_rate_of_change_raw(returns_array, LenST, LenLT)
    median_roc_raw_sma = rolling_mean(median_roc_raw, length=MacdLength, min_length=MacdLength)

    return (median_roc_raw - median_roc_raw_sma)


def calculate_central_rate_of_change_macd_raw(returns_array: ArrayFloat, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
    central_roc_raw = calculate_central_rate_of_change_raw(returns_array, LenST, LenLT)
    central_roc_raw_sma = rolling_mean(central_roc_raw, length=MacdLength, min_length=MacdLength)

    return (central_roc_raw - central_roc_raw_sma)


def smoothed_skewness(returns_array: ArrayFloat, LenSmooth: int, LenSkew: int) -> ArrayFloat:
    smoothed_array = rolling_mean(returns_array, length=LenSmooth, min_length=LenSmooth)

    return rolling_skewness(smoothed_array, length=LenSkew, min_length=LenSkew)


def smoothed_kurtosis(returns_array: ArrayFloat, LenSmooth: int, LenSkew: int) -> ArrayFloat:
    smoothed_array = rolling_mean(returns_array, length=LenSmooth, min_length=LenSmooth)

    return rolling_kurtosis(smoothed_array, length=LenSkew, min_length=LenSkew)


def smoothed_directional_volatility(returns_array: ArrayFloat, LenST: int, LenVol: int) -> ArrayFloat:
    smoothed_array = rolling_mean(returns_array, length=LenST, min_length=LenST)
    positive_vol, negative_vol = separate_volatility(smoothed_array, LenVol)

    return (positive_vol - negative_vol)