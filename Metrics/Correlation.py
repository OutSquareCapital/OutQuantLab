from Utilitary import ArrayFloat, Float32
import numpy as np

def calculate_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    return np.corrcoef(returns_array, rowvar=False, dtype=Float32)

def calculate_overall_average_correlation(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    sum_correlations: ArrayFloat = np.sum(corr_matrix, axis=1)
    sum_without_diagonal: ArrayFloat = sum_correlations - 1
    mean_correlations: ArrayFloat = sum_without_diagonal / (corr_matrix.shape[1] - 1)
    return mean_correlations