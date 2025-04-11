from numquant.main import Float2D, Float32, Nan, np


def get_correlation_matrix(returns_array: Float2D) -> Float2D:
    return np.corrcoef(returns_array, rowvar=False, dtype=Float32)


def get_distance_matrix(returns_array: Float2D) -> Float2D:
    corr_matrix: Float2D = get_correlation_matrix(returns_array=returns_array)
    distance_matrix: Float2D = 2 * (1 - corr_matrix)
    return np.sqrt(distance_matrix, out=corr_matrix, dtype=Float32)

def get_average_correlation(returns_array: Float2D) -> Float2D:
    corr_matrix: Float2D = get_correlation_matrix(returns_array=returns_array)
    sum_correlations: Float2D = np.sum(corr_matrix, axis=1)
    sum_without_diagonal: Float2D = sum_correlations - 1
    return sum_without_diagonal / (corr_matrix.shape[1] - 1)


def get_filled_correlation_matrix(returns_array: Float2D) -> Float2D:
    corr_matrix: Float2D = get_correlation_matrix(returns_array=returns_array)
    np.fill_diagonal(a=corr_matrix, val=Nan)
    return corr_matrix
