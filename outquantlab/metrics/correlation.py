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


def get_clusters(
    returns_array: arrays.Float2D, asset_names: list[str], max_clusters: int
) -> dict[str, list[str]]:
    clusters_structure: list[int] = get_cluster_structure(
        returns_array=returns_array, max_clusters=max_clusters
    )

    return _get_clusters_dict(
        max_clusters=max_clusters, asset_names=asset_names, clusters_structure=clusters_structure
    )


def _get_clusters_dict(
    max_clusters: int, asset_names: list[str], clusters_structure: list[int]
) -> dict[str, list[str]]:
    return {
        str(object=cluster_id): _get_cluster_names(
            cluster_id=cluster_id, asset_names=asset_names, clusters_structure=clusters_structure
        )
        for cluster_id in range(1, max_clusters + 1)
    }


def _get_cluster_names(
    cluster_id: int, asset_names: list[str], clusters_structure: list[int]
) -> list[str]:
    return [
        asset
        for asset, cluster in zip(asset_names, clusters_structure)
        if cluster == cluster_id
    ]
