import numpy as np
from Metrics.Aggregation import rolling_mean, rolling_median, rolling_min, rolling_max
from Metrics.Volatility import rolling_volatility
from Utilitary import ArrayFloat, Float32

def ratio_normalization(nominator: ArrayFloat, denominator: ArrayFloat) -> ArrayFloat:
    return (nominator / denominator) - Float32(1.0)

def sign_normalization(signal_array: ArrayFloat) -> ArrayFloat:
    return np.sign(signal_array, out=signal_array)

def relative_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    return signal_array - rolling_mean(array=signal_array, length=length, min_length=1)

def z_score_normalization(signal_array: ArrayFloat, length: int) -> ArrayFloat:
    relative_data: ArrayFloat = relative_normalization(signal_array=signal_array, length=length)
    std_data: ArrayFloat = rolling_volatility(array=signal_array, length=length, min_length=1)
    return relative_data / std_data

def calculate_indicator_on_trend_signal(
    trend_signal: ArrayFloat, 
    indicator_signal: ArrayFloat
    ) -> ArrayFloat:
    limit: Float32 = Float32(0.0)
    return np.where(
        ((trend_signal < limit) & (indicator_signal > limit)) | 
        ((trend_signal > limit) & (indicator_signal < limit)), limit, 
        indicator_signal
    )

def rolling_median_normalisation(
    signal_array: ArrayFloat, 
    window_length: int, 
    limit:int = 1
    ) -> ArrayFloat:
    adjusted_signal_array: ArrayFloat = np.empty_like(prototype=signal_array)
    median_array: ArrayFloat = rolling_median(array=signal_array, length=window_length, min_length=window_length)
    max_array: ArrayFloat = rolling_max(array=signal_array, length=window_length, min_length=window_length)
    min_array: ArrayFloat  =  rolling_min(array=signal_array, length=window_length, min_length=window_length)

    adjusted_signal_array= ((signal_array - median_array) / (max_array - min_array)) * Float32(2.0)

    return np.clip(adjusted_signal_array, -limit, limit)