from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.config_classes.collections import Asset
from outquantlab.config_classes.generic_classes import BaseClustersTree
from outquantlab.indicators import BaseIndic
from outquantlab.metrics import calculate_distance_matrix
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat
from enum import StrEnum

class Prefix(StrEnum):
    ASSET = "Asset"
    INDIC = "Indic"

class AssetsClusters(BaseClustersTree):
    def __init__(self, clusters: dict[str, dict[str, list[str]]]) -> None:
        super().__init__(clusters=clusters, prefix=Prefix.ASSET)

    def get_clusters_tuples(self, entities: list[Asset]) -> list[tuple[str, ...]]:
        assets_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [(*assets_to_clusters[asset.name], asset.name) for asset in entities]


class IndicsClusters(BaseClustersTree):
    def __init__(self, clusters: dict[str, dict[str, list[str]]]) -> None:
        super().__init__(clusters=clusters, prefix=Prefix.INDIC)

    def get_clusters_tuples(self, entities: list[BaseIndic]) -> list[tuple[str, ...]]:
        indics_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [
            (*indics_to_clusters[indic.name], indic.name, "_".join(map(str, combo)))
            for indic in entities
            for combo in indic.param_combos
        ]


def generate_dynamic_clusters(
    returns_df: DataFrameFloat, max_clusters: int
) -> dict[str, list[str]]:
    flat_clusters: list[int] = _get_flat_clusters(
        returns_array=returns_df.get_array(), max_clusters=max_clusters
    )
    asset_names: list[str] = returns_df.columns.tolist()

    return _assign_clusters(
        max_clusters=max_clusters, asset_names=asset_names, flat_clusters=flat_clusters
    )


def _assign_clusters(
    max_clusters: int, asset_names: list[str], flat_clusters: list[int]
) -> dict[str, list[str]]:
    return {
        str(object=cluster_id): _get_assets_in_cluster(
            cluster_id=cluster_id, asset_names=asset_names, flat_clusters=flat_clusters
        )
        for cluster_id in range(1, max_clusters + 1)
    }


def _get_assets_in_cluster(
    cluster_id: int, asset_names: list[str], flat_clusters: list[int]
) -> list[str]:
    return [
        asset
        for asset, cluster in zip(asset_names, flat_clusters)
        if cluster == cluster_id
    ]


def _get_flat_clusters(returns_array: ArrayFloat, max_clusters: int) -> list[int]:
    distance_matrix: ArrayFloat = calculate_distance_matrix(returns_array=returns_array)
    distance_condensed: ArrayFloat = squareform(distance_matrix, checks=False)
    linkage_matrix: ArrayFloat = linkage(distance_condensed, method="ward")  # type: ignore
    return fcluster(linkage_matrix, max_clusters, criterion="maxclust")  # type: ignore
