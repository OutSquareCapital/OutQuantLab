from abc import ABC, abstractmethod

from outquantlab.indicators import GenericIndic
from typing import NamedTuple, Protocol
from dataclasses import dataclass

@dataclass(slots=True)
class Asset:
    name: str
    active: bool




class StrategyComponent(Protocol):
    name: str
    active: bool

class AssetsClustersTuples(NamedTuple):
    cluster: str
    asset: str


class IndicsClustersTuples(NamedTuple):
    cluster: str
    indics: str
    params: str

type ClustersTree = dict[str, list[str]]
type ClustersMap = dict[str, str]

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