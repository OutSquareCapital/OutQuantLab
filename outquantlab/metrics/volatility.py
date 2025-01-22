import numpy as np
from outquantlab.typing_conventions import ArrayFloat
import bottleneck as bn # type: ignore
from outquantlab.metrics.aggregation import rolling_mean, rolling_median
from outquantlab.metrics.maths_constants import ANNUALIZED_PERCENTAGE_FACTOR

def overall_volatility(returns_array: ArrayFloat) -> ArrayFloat:
    return bn.nanstd(returns_array, axis=0, ddof=1) # type: ignore

def overall_volatility_annualized(returns_array: ArrayFloat) -> ArrayFloat:
    return overall_volatility(returns_array=returns_array) * ANNUALIZED_PERCENTAGE_FACTOR

def rolling_volatility(array: ArrayFloat, length: int, min_length: int = 1) -> ArrayFloat:
    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof = 1) # type: ignore

def hv_short_term(
    returns_array: ArrayFloat, 
    lengths_list: list[int]
    ) -> ArrayFloat:

    hv_arrays: ArrayFloat = np.array([
        rolling_volatility(
        returns_array, 
        length=length, 
        min_length=4)
        for length in lengths_list])

    return np.mean(hv_arrays, axis=0)

def hv_long_term(
    short_term_vol_array: ArrayFloat, 
    long_term_lengths: list[int]
    ) -> ArrayFloat:
    
    long_term_vol_arrays = np.array([
        rolling_median(
        short_term_vol_array, 
        length=length, 
        min_length=1)
        for length in long_term_lengths])

    return np.mean(long_term_vol_arrays, axis=0)

def hv_composite(
    returns_array: ArrayFloat, 
    short_term_lengths: list[int]=[8, 16, 32, 64], 
    long_term_lengths: list[int]=[256, 512, 1024, 2048, 4096], 
    st_weight: float =0.6
    ) -> ArrayFloat:

    max_length: int = returns_array.shape[0]
    adjusted_lengths: list[int] = [length for length in long_term_lengths if length < max_length]
    
    short_term_vol_array = hv_short_term(returns_array, lengths_list=short_term_lengths)
    long_term_vol_array = hv_long_term(short_term_vol_array, long_term_lengths=adjusted_lengths)
    lt_weight = 1 - st_weight
    
    composite_vol_array = ((st_weight * short_term_vol_array) + (lt_weight * long_term_vol_array)) * ANNUALIZED_PERCENTAGE_FACTOR
    return rolling_mean(composite_vol_array, length=4, min_length=1)

def separate_volatility(array:ArrayFloat, LenVol: int) -> tuple[ArrayFloat, ArrayFloat]:

    positive_returns = np.where(np.isnan(array), np.nan, np.where(array > 0, array, 0))
    negative_returns = np.where(np.isnan(array), np.nan, np.where(array < 0, array, 0))

    vol_positive = rolling_volatility(positive_returns, length=LenVol, min_length=1)
    vol_negative = rolling_volatility(negative_returns, length=LenVol, min_length=1)

    return vol_positive, vol_negative

