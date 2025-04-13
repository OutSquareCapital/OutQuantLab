from abc import ABC, abstractmethod

from pandas import MultiIndex

from outquantlab.indicators import GenericIndic
from outquantlab.portfolio.structures import (
    CLUSTERS_LEVELS,
    Asset,
    AssetsClustersTuples,
    ClustersMap,
    ClustersTree,
    ColumnName,
    IndicsClustersTuples,
    PortfolioClustersTuples,
    StrategyComponent,
)


class BaseClustersTree[T: StrategyComponent, L: tuple[str, ...]](ABC):
    def __init__(self, clusters: ClustersTree) -> None:
        self.structure: ClustersTree = clusters
        self.mapping: ClustersMap = self.map_nested_clusters_to_entities()

    def check_data_structure(self, entities: list[T]) -> None:
        if "default" not in self.structure:
            self.structure["default"] = []
        for entity in entities:
            if entity.name not in self.mapping:
                self.structure["default"].append(entity.name)
                self.mapping[entity.name] = "default"

    def update_clusters_structure(self, new_structure: ClustersTree) -> None:
        self.structure = new_structure
        self.mapping = self.map_nested_clusters_to_entities()

    def map_nested_clusters_to_entities(self) -> ClustersMap:
        return {
            entity: level1
            for level1, entities in self.structure.items()
            for entity in entities
        }

    @abstractmethod
    def get_clusters_tuples(self, entities: list[T]) -> list[L]: ...


class AssetsClusters(BaseClustersTree[Asset, AssetsClustersTuples]):
    def get_clusters_tuples(self, entities: list[Asset]) -> list[AssetsClustersTuples]:
        return [AssetsClustersTuples(*self.mapping[asset.name]) for asset in entities]


class IndicsClusters(BaseClustersTree[GenericIndic, IndicsClustersTuples]):
    def get_clusters_tuples(
        self, entities: list[GenericIndic]
    ) -> list[IndicsClustersTuples]:
        return [
            IndicsClustersTuples(
                *self.mapping[indic.name], params="_".join(map(str, combo))
            )
            for indic in entities
            for combo in indic.combos
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


def get_multi_index(asset_names: list[str], indics: list[GenericIndic]) -> MultiIndex:
    return MultiIndex.from_tuples(  # type: ignore
        tuples=get_categories(asset_names=asset_names, indics=indics),
        names=CLUSTERS_LEVELS,
    )

def get_categories(asset_names: list[str], indics: list[GenericIndic]) -> list[ColumnName]:
    return [
            ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.get_combo_names()
            for asset_name in asset_names
        ]