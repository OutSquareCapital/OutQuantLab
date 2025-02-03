from outquantlab.typing_conventions import ArrayFloat, Float32
from numpy import corrcoef, sqrt, sum


def calculate_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    return corrcoef(returns_array, rowvar=False, dtype=Float32)


def calculate_distance_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    return sqrt(2 * (1 - corr_matrix))


def calculate_overall_average_correlation(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    sum_correlations: ArrayFloat = sum(corr_matrix, axis=1)
    sum_without_diagonal: ArrayFloat = sum_correlations - 1
    return sum_without_diagonal / (corr_matrix.shape[1] - 1)
