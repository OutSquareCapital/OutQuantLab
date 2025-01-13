from TypingConventions import ArrayFloat, Float32
import numpy as np

def calculate_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    return np.corrcoef(returns_array, rowvar=False, dtype=Float32)

def calculate_distance_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    return np.sqrt(2 * (1 - corr_matrix))

def calculate_overall_average_correlation(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    sum_correlations: ArrayFloat = np.sum(corr_matrix, axis=1)
    sum_without_diagonal: ArrayFloat = sum_correlations - 1
    return sum_without_diagonal / (corr_matrix.shape[1] - 1)