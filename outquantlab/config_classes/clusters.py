from enum import StrEnum

from outquantlab.config_classes.collections import Asset
from outquantlab.config_classes.generic_classes import BaseClustersTree
from outquantlab.indicators import BaseIndic


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

def assign_clusters(
    max_clusters: int, asset_names: list[str], flat_clusters: list[int]
) -> dict[str, list[str]]:
    print(flat_clusters)
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
