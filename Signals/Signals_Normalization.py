import numexpr as ne # type: ignore
import numpy as np
from Metrics import rolling_mean, rolling_median, rolling_min, rolling_max, rolling_volatility
from Infrastructure import bfill
from numpy.typing import NDArray

def ratio_normalization(nominator: NDArray[np.float32], denominator: NDArray[np.float32]) -> NDArray[np.float32]:
    return (nominator / denominator) - 1

def sign_normalization(signal_array: NDArray[np.float32]) -> NDArray[np.float32]:
    return np.sign(signal_array, out=signal_array)

def relative_normalization(signal_array: NDArray[np.float32], length: int) -> NDArray[np.float32]:
    average_signal = rolling_mean(signal_array, length=length, min_length=1)
    return signal_array - average_signal

def calculate_indicator_on_trend_signal(trend_signal: NDArray[np.float32], indicator_signal: NDArray[np.float32]) -> NDArray[np.float32]:
    return np.where(
        ((trend_signal < 0) & (indicator_signal > 0)) | 
        ((trend_signal > 0) & (indicator_signal < 0)), 0, 
        indicator_signal
    )

def rolling_median_normalisation(
    signal_array: NDArray[np.float32], 
    window_length: int, 
    limit:int = 1
    ) -> NDArray[np.float32]:

    adjusted_signal_array = np.empty_like(signal_array, dtype=np.float32)
    dict = {
        "signal_array": signal_array,
        "median_array": rolling_median(signal_array, length=window_length, min_length=window_length),
        "max": rolling_min(signal_array, length=window_length, min_length=window_length),
        "min": rolling_max(signal_array, length=window_length, min_length=window_length)
    }
    ne.evaluate("((signal_array - median_array) / (max - min)) * 2", out=adjusted_signal_array, local_dict=dict) # type: ignore

    return np.clip(adjusted_signal_array, -limit, limit)

def rolling_std_normalisation(
    signal_array: NDArray[np.float32], 
    window_length: int, 
    limit:int = 1
    ) -> NDArray[np.float32]:

    adjusted_signal_array = np.empty_like(signal_array, dtype=np.float32)
    dict = {
        "signal_array": signal_array,
        "median_array": rolling_median(signal_array, length=window_length, min_length=window_length),
        "rolling_std": rolling_volatility(signal_array, length=window_length, min_length=window_length)
    }
    ne.evaluate("((signal_array - median_array) / rolling_std) * 0.5", out=adjusted_signal_array, local_dict=dict) # type: ignore
    
    return np.clip(adjusted_signal_array, -limit, limit)

def rolling_scalar_normalisation(
    signal_array: NDArray[np.float32], 
    window_length: int, 
    scalar:int = 1, 
    limit:int = 2
    ) -> NDArray[np.float32]:
    row_mean_array = np.nanmean(np.abs(signal_array), axis=1)
    median = rolling_median(row_mean_array, length=window_length, min_length=1)
    median = bfill(median)
    normalization_factor = scalar / median[:, None]
    return np.clip(signal_array * normalization_factor, -limit, limit)
