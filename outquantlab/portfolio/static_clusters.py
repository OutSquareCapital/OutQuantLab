from pandas import MultiIndex
from outquantlab.portfolio.interfaces import BaseClustersTree
from outquantlab.indicators import BaseIndic
from outquantlab.portfolio.levels import (
    CLUSTERS_LEVELS,
    PortfolioClustersTuples,
    AssetsClustersTuples,
    IndicsClustersTuples,
)
from dataclasses import dataclass

@dataclass(slots=True)
class Asset:
    name: str
    active: bool


class AssetsClusters(BaseClustersTree[Asset, AssetsClustersTuples]):
    def get_clusters_tuples(self, entities: list[Asset]) -> list[AssetsClustersTuples]:
        return [
            AssetsClustersTuples(*self.mapping[asset.name])
            for asset in entities
        ]


class IndicsClusters(BaseClustersTree[BaseIndic, IndicsClustersTuples]):
    def get_clusters_tuples(
        self, entities: list[BaseIndic]
    ) -> list[IndicsClustersTuples]:
        return [
            IndicsClustersTuples(
                *self.mapping[indic.name], params="_".join(map(str, combo))
            )
            for indic in entities
            for combo in indic.params.combos
        ]


class ClustersHierarchy:
    def __init__(
        self,
        asset_tuples: list[AssetsClustersTuples],
        indics_tuples: list[IndicsClustersTuples],
    ) -> None:
        self.product_tuples: list[PortfolioClustersTuples] = [
            PortfolioClustersTuples(
                *asset_tuple,
                *indics_tuple,
            )
            for indics_tuple in indics_tuples
            for asset_tuple in asset_tuples
        ]
    def get_multi_index(self) -> MultiIndex:
        return MultiIndex.from_tuples(  # type: ignore
            tuples=self.product_tuples,
            names=CLUSTERS_LEVELS,
        )
    
    @property
    def length(self) -> int:
        return len(self.product_tuples)
