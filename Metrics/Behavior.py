import numpy as np
from Infrastructure import Fast_Tools as ft
from Metrics.Aggregation import rolling_mean

def rolling_autocorrelation(returns_array: np.ndarray, length: int) -> np.ndarray:

    # Moyennes roulantes
    mean = rolling_mean(returns_array, length=length, min_length=20)

    shifted_array = ft.shift_array(returns_array)

    # Déviations roulantes
    deviations = returns_array - mean
    deviations_shifted = shifted_array - mean

    # Covariance roulante
    rolling_covariance = rolling_mean(deviations * deviations_shifted, length=length, min_length=20)

    # Variances roulantes
    rolling_variance = rolling_mean(deviations ** 2, length=length, min_length=20)
    rolling_variance_shifted = rolling_mean(deviations_shifted ** 2, length=length, min_length=20)

    autocorr_result = rolling_covariance / np.sqrt(rolling_variance * rolling_variance_shifted)

    autocorr_mean = rolling_mean(autocorr_result, length=250, min_length=1)

    return autocorr_mean