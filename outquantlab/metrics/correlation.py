from numpy import corrcoef, sqrt, sum, fill_diagonal, nan
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.structures import ArrayFloat, Float32


def get_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    return corrcoef(returns_array, rowvar=False, dtype=Float32)


def get_distance_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = get_correlation_matrix(returns_array=returns_array)
    distance_matrix: ArrayFloat = 2 * (1 - corr_matrix)
    return sqrt(distance_matrix, out=corr_matrix, dtype=Float32)

def get_overall_average_correlation(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = get_correlation_matrix(returns_array=returns_array)
    sum_correlations: ArrayFloat = sum(corr_matrix, axis=1)
    sum_without_diagonal: ArrayFloat = sum_correlations - 1
    return sum_without_diagonal / (corr_matrix.shape[1] - 1)


def get_filled_correlation_matrix(returns_array: ArrayFloat) -> ArrayFloat:
    corr_matrix: ArrayFloat = get_correlation_matrix(returns_array=returns_array)
    fill_diagonal(a=corr_matrix, val=nan)
    return corr_matrix


def get_clusters(
    returns_array: ArrayFloat, asset_names: list[str], max_clusters: int
) -> dict[str, list[str]]:
    clusters_structure: list[int] = _get_cluster_structure(
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


def _get_cluster_structure(returns_array: ArrayFloat, max_clusters: int) -> list[int]:
    distance_matrix: ArrayFloat = get_distance_matrix(returns_array=returns_array)
    distance_condensed: ArrayFloat = squareform(distance_matrix, checks=False)
    linkage_matrix: ArrayFloat = linkage(distance_condensed, method="ward")  # type: ignore
    return fcluster(linkage_matrix, max_clusters, criterion="maxclust")  # type: ignore
