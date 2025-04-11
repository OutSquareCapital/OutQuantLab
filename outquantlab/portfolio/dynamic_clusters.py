import numquant as nq

def get_clusters(
    returns_array: nq.Float2D, asset_names: list[str], max_clusters: int
) -> dict[str, list[str]]:
    clusters_structure: list[int] = nq.metrics.get_cluster_structure(
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
