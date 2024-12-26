import numpy as np
from Infrastructure import shift_array
from Metrics.Aggregation import rolling_mean
from Files import NDArrayFloat

def rolling_autocorrelation(returns_array: NDArrayFloat, length: int) -> NDArrayFloat:

    mean = rolling_mean(returns_array, length=length, min_length=20)

    shifted_array = shift_array(returns_array)

    deviations = returns_array - mean
    deviations_shifted = shifted_array - mean

    rolling_covariance = rolling_mean(deviations * deviations_shifted, length=length, min_length=20)

    rolling_variance = rolling_mean(deviations ** 2, length=length, min_length=20)
    rolling_variance_shifted = rolling_mean(deviations_shifted ** 2, length=length, min_length=20)

    autocorr_result = rolling_covariance / np.sqrt(rolling_variance * rolling_variance_shifted)

    autocorr_mean = rolling_mean(autocorr_result, length=250, min_length=1)

    return autocorr_mean