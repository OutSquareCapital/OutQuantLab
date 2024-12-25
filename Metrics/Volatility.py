import numpy as np
from numpy.typing import NDArray
from Files import ANNUALIZED_PERCENTAGE_FACTOR
import bottleneck as bn
from Metrics.Aggregation import rolling_mean, rolling_median

def rolling_volatility(array: NDArray[np.float32], length: int, min_length: int = 1) -> NDArray[np.float32]:

    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof = 1)

def hv_short_term(
    returns_array: NDArray[np.float32], 
    lengths_list: list[int]
    ) -> NDArray[np.float32]:

    hv_arrays = np.array([
        rolling_volatility(
        returns_array, 
        length=length, 
        min_length=4)
        for length in lengths_list])

    return np.mean(hv_arrays, axis=0)

def hv_long_term(
    short_term_vol_array: NDArray[np.float32], 
    long_term_lengths: list[int]
    ) -> NDArray[np.float32]:
    
    long_term_vol_arrays = np.array([
        rolling_median(
        short_term_vol_array, 
        length=length, 
        min_length=1)
        for length in long_term_lengths])

    return np.mean(long_term_vol_arrays, axis=0)

def hv_composite(
    returns_array: NDArray[np.float32], 
    short_term_lengths=[8, 16, 32, 64], 
    long_term_lengths=[256, 512, 1024, 2048, 4096], 
    st_weight=0.6
    ) -> NDArray[np.float32]:

    max_length = returns_array.shape[0]
    adjusted_lengths = [length for length in long_term_lengths if length < max_length]
    
    short_term_vol_array = hv_short_term(returns_array, lengths_list=short_term_lengths)

    long_term_vol_array = hv_long_term(short_term_vol_array, long_term_lengths=adjusted_lengths)

    lt_weight = 1 - st_weight
    
    composite_vol_array = ((st_weight * short_term_vol_array) + (lt_weight * long_term_vol_array)) * ANNUALIZED_PERCENTAGE_FACTOR

    return rolling_mean(composite_vol_array, length=4, min_length=1)

def separate_volatility(array:np.ndarray, LenVol: int) -> tuple[np.ndarray, np.ndarray]:

    positive_returns = np.where(np.isnan(array), np.nan, np.where(array > 0, array, 0))
    negative_returns = np.where(np.isnan(array), np.nan, np.where(array < 0, array, 0))

    vol_positive = rolling_volatility(positive_returns, length=LenVol, min_length=1)
    vol_negative = rolling_volatility(negative_returns, length=LenVol, min_length=1)

    return vol_positive, vol_negative

