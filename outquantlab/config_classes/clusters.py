from outquantlab.config_classes.collections import Asset
from outquantlab.config_classes.generic_classes import BaseClustersTree
from outquantlab.indicators import BaseIndic


class AssetsClusters(BaseClustersTree[Asset]):
    def get_clusters_tuples(self, entities: list[Asset]) -> list[tuple[str, ...]]:
        assets_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [(*assets_to_clusters[asset.name], asset.name) for asset in entities]


class IndicsClusters(BaseClustersTree[BaseIndic]):
    def get_clusters_tuples(self, entities: list[BaseIndic]) -> list[tuple[str, ...]]:
        indics_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [
            (*indics_to_clusters[indic.name], indic.name, "_".join(map(str, combo)))
            for indic in entities
            for combo in indic.params.combos
        ]
