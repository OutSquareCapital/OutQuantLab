from outquantlab.config_classes.collections import Asset
from outquantlab.config_classes.generic_classes import BaseClustersTree
from outquantlab.indicators import BaseIndic


class AssetsClusters(BaseClustersTree[Asset]):
    def get_clusters_tuples(self, entities: list[Asset]) -> list[tuple[str, ...]]:
        return [(*self.mapping[asset.name], asset.name) for asset in entities]


class IndicsClusters(BaseClustersTree[BaseIndic]):
    def get_clusters_tuples(self, entities: list[BaseIndic]) -> list[tuple[str, ...]]:
        return [
            (*self.mapping[indic.name], indic.name, "_".join(map(str, combo)))
            for indic in entities
            for combo in indic.params.combos
        ]
