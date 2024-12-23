import numpy as np
from Files import ANNUALIZED_PERCENTAGE_FACTOR
import bottleneck as bn
from Metrics.Aggregation import rolling_mean, rolling_median

def rolling_volatility(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof = 1)

def hv_short_term(returns_array: np.ndarray, lengths_list=[8, 16, 32, 64]) -> np.ndarray:

    hv_arrays = np.array([rolling_volatility(
        returns_array, 
        length=length, 
        min_length=length)
        for length in lengths_list])

    return np.nanmean(hv_arrays, axis=0)

def hv_long_term(short_term_vol_array: np.ndarray, long_term_lengths=[200, 400, 800, 1600, 3200]) -> np.ndarray:
    max_length = short_term_vol_array.shape[0]
    adjusted_lengths = [min(length, max_length) for length in long_term_lengths]
    long_term_vol_arrays = np.array([rolling_median(
        short_term_vol_array, 
        length=length, 
        min_length=1)
        for length in adjusted_lengths])

    return np.nanmean(long_term_vol_arrays, axis=0)

def hv_composite(
    returns_array: np.ndarray, 
    lengths=[8, 16, 32, 64], 
    long_term_lengths=[200, 400, 800, 1600, 3200], 
    st_weight=0.6, 
    annualization=True) -> np.ndarray:

    short_term_vol_array = hv_short_term(returns_array, lengths_list=lengths)

    long_term_vol_array = hv_long_term(short_term_vol_array, long_term_lengths=long_term_lengths)

    lt_weight = 1 - st_weight
    composite_vol_array = (st_weight * short_term_vol_array) + (lt_weight * long_term_vol_array)

    if annualization:

        composite_vol_array = composite_vol_array * ANNUALIZED_PERCENTAGE_FACTOR

    return rolling_mean(composite_vol_array, length=5)

def separate_volatility(array:np.ndarray, LenVol: int) -> tuple[np.ndarray, np.ndarray]:

    positive_returns = np.where(np.isnan(array), np.nan, np.where(array > 0, array, 0))
    negative_returns = np.where(np.isnan(array), np.nan, np.where(array < 0, array, 0))

    vol_positive = rolling_volatility(positive_returns, length=LenVol, min_length=1)
    vol_negative = rolling_volatility(negative_returns, length=LenVol, min_length=1)

    return vol_positive, vol_negative

