from numpy import corrcoef, sqrt, sum, fill_diagonal
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.structures import arrays


def get_correlation_matrix(returns_array: arrays.Float2D) -> arrays.Float2D:
    return corrcoef(returns_array, rowvar=False, dtype=arrays.Float32)


def get_distance_matrix(returns_array: arrays.Float2D) -> arrays.Float2D:
    corr_matrix: arrays.Float2D = get_correlation_matrix(returns_array=returns_array)
    distance_matrix: arrays.Float2D = 2 * (1 - corr_matrix)
    return sqrt(distance_matrix, out=corr_matrix, dtype=arrays.Float32)

def get_overall_average_correlation(returns_array: arrays.Float2D) -> arrays.Float2D:
    corr_matrix: arrays.Float2D = get_correlation_matrix(returns_array=returns_array)
    sum_correlations: arrays.Float2D = sum(corr_matrix, axis=1)
    sum_without_diagonal: arrays.Float2D = sum_correlations - 1
    return sum_without_diagonal / (corr_matrix.shape[1] - 1)


def get_filled_correlation_matrix(returns_array: arrays.Float2D) -> arrays.Float2D:
    corr_matrix: arrays.Float2D = get_correlation_matrix(returns_array=returns_array)
    fill_diagonal(a=corr_matrix, val=arrays.Nan)
    return corr_matrix



def get_cluster_structure(returns_array: arrays.Float2D, max_clusters: int) -> list[int]:
    distance_matrix: arrays.Float2D = get_distance_matrix(returns_array=returns_array)
    distance_condensed: arrays.Float2D = squareform(distance_matrix, checks=False)
    linkage_matrix: arrays.Float2D = linkage(distance_condensed, method="ward")  # type: ignore
    return fcluster(linkage_matrix, max_clusters, criterion="maxclust")  # type: ignore