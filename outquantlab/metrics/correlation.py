from numpy import corrcoef, sqrt, sum, fill_diagonal, nan
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.typing_conventions import ArrayFloat, Float32


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


def get_corr_clusters(returns_array: ArrayFloat, max_clusters: int) -> list[int]:
    distance_matrix: ArrayFloat = calculate_distance_matrix(returns_array=returns_array)
    distance_condensed: ArrayFloat = squareform(distance_matrix, checks=False)
    linkage_matrix: ArrayFloat = linkage(distance_condensed, method="ward")  # type: ignore
    return fcluster(linkage_matrix, max_clusters, criterion="maxclust")  # type: ignore


def get_filled_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = calculate_correlation_matrix(returns_array=returns_array)
    fill_diagonal(a=corr_matrix, val=nan)
    return corr_matrix
