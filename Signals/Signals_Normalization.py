import numexpr as ne
import numpy as np
import Metrics as mt
from Infrastructure import Fast_Tools as ft

def ratio_normalization(nominator: np.ndarray, denominator: np.ndarray) -> np.ndarray:

    return (nominator/denominator) - 1

def sign_normalization(signal_array:np.ndarray) -> np.ndarray:

    return np.sign(signal_array, out=signal_array)

def relative_normalization(signal_array: np.ndarray, length: int) -> np.ndarray:
        
    average_signal = mt.rolling_mean(signal_array, length=length, min_length=1)

    return (signal_array - average_signal)
    
def calculate_indicator_on_trend_signal(trend_signal:np.ndarray, indicator_signal:np.ndarray) -> np.ndarray:

    return np.where(
        ((trend_signal < 0) & (indicator_signal > 0)) | 
        ((trend_signal > 0) & (indicator_signal < 0)), 0, 
        indicator_signal
    )

def rolling_median_normalisation(signal_array: np.ndarray, window_length: int) -> np.ndarray:

    limit = 1

    median_array = mt.rolling_median(signal_array, length=window_length, min_length=window_length)
    
    rolling_min = mt.rolling_min(signal_array, length=window_length, min_length=window_length)
    rolling_max = mt.rolling_max(signal_array, length=window_length, min_length=window_length)
    
    adjusted_signal_array = np.empty_like(signal_array, dtype=np.float32)
    ne.evaluate("((signal_array - median_array) / (rolling_max - rolling_min)) * 2", out=adjusted_signal_array)

    return np.clip(adjusted_signal_array, -limit, limit)

def rolling_std_normalisation(signal_array: np.ndarray, window_length: int) -> np.ndarray:

    limit = 1

    median_array = mt.rolling_median(signal_array, length=window_length, min_length=window_length)
    
    rolling_std = mt.rolling_volatility(signal_array, length=window_length, min_length=window_length)
    
    adjusted_signal_array = np.empty_like(signal_array, dtype=np.float32)
    
    ne.evaluate("((signal_array - median_array) / rolling_std) * 0.5", out=adjusted_signal_array)

    return np.clip(adjusted_signal_array, -limit, limit)

def rolling_scalar_normalisation(signal_array: np.ndarray, window_length: int) -> np.ndarray:

    scalar = 1
    limit = 2

    row_mean_array = np.nanmean(np.abs(signal_array), axis=1)

    rolling_median = mt.rolling_median(row_mean_array, length=window_length, min_length=1)

    rolling_median = ft.bfill(rolling_median)

    adjusted_signal_array = np.empty_like(signal_array, dtype=np.float32)

    normalization_factor = scalar / rolling_median[:, None]

    return np.clip(signal_array * normalization_factor, -limit, limit)