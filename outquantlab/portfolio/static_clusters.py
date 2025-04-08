from pandas import MultiIndex
from outquantlab.indicators import BaseIndic
import outquantlab.portfolio.structures as structs
from abc import ABC, abstractmethod

class BaseClustersTree[T: structs.StrategyComponent, L: tuple[str, ...]](ABC):
    def __init__(self, clusters: structs.ClustersTree) -> None:
        self.structure: structs.ClustersTree = clusters
        self.mapping: structs.ClustersMap = self.map_nested_clusters_to_entities()

    def check_data_structure(self, entities: list[T]) -> None:
        if "default" not in self.structure:
            self.structure["default"] = []
        for entity in entities:
            if entity.name not in self.mapping:
                self.structure["default"].append(entity.name)
                self.mapping[entity.name] = ("default")

    def update_clusters_structure(self, new_structure: structs.ClustersTree) -> None:
        self.structure = new_structure
        self.mapping = self.map_nested_clusters_to_entities()

    def map_nested_clusters_to_entities(self) -> structs.ClustersMap:
        return {
            entity: level1
            for level1, entities in self.structure.items()
            for entity in entities
        }

    @abstractmethod
    def get_clusters_tuples(self, entities: list[T]) -> list[L]: ...


class AssetsClusters(BaseClustersTree[structs.Asset, structs.AssetsClustersTuples]):
    def get_clusters_tuples(self, entities: list[structs.Asset]) -> list[structs.AssetsClustersTuples]:
        return [
            structs.AssetsClustersTuples(*self.mapping[asset.name])
            for asset in entities
        ]


class IndicsClusters(BaseClustersTree[BaseIndic, structs.IndicsClustersTuples]):
    def get_clusters_tuples(
        self, entities: list[BaseIndic]
    ) -> list[structs.IndicsClustersTuples]:
        return [
            structs.IndicsClustersTuples(
                *self.mapping[indic.name], params="_".join(map(str, combo))
            )
            for indic in entities
            for combo in indic.params.combos
        ]


class ClustersHierarchy:
    def __init__(
        self,
        asset_tuples: list[structs.AssetsClustersTuples],
        indics_tuples: list[structs.IndicsClustersTuples],
    ) -> None:
        self.product_tuples: list[structs.PortfolioClustersTuples] = [
            structs.PortfolioClustersTuples(
                *asset_tuple,
                *indics_tuple,
            )
            for indics_tuple in indics_tuples
            for asset_tuple in asset_tuples
        ]
    def get_multi_index(self) -> MultiIndex:
        return MultiIndex.from_tuples(  # type: ignore
            tuples=self.product_tuples,
            names=structs.CLUSTERS_LEVELS,
        )
    
    @property
    def length(self) -> int:
        return len(self.product_tuples)


def get_multi_index(asset_names: list[str], indics: list[BaseIndic]) -> MultiIndex:
    return MultiIndex.from_tuples(  # type: ignore
        tuples=[
            structs.ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.params.get_combo_names()
            for asset_name in asset_names
        ],
        names=structs.CLUSTERS_LEVELS
    )
