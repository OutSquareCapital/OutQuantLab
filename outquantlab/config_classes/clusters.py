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
