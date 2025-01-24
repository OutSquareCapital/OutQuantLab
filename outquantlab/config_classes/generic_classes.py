from typing import Generic, Any, TypeVar
from abc import ABC, abstractmethod
from outquantlab.typing_conventions import StrategyComponent, ClustersHierarchy

T = TypeVar("T", bound=StrategyComponent)

class BaseCollection(ABC, Generic[T]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.entities: dict[str, T] = {} 
        self._load_entities(*args, **kwargs)

    @abstractmethod
    def _load_entities(self, *args: Any, **kwargs: Any) -> None: ...

    def get_all_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    def get_all_active_entities(self) -> list[T]:
        return [entity for entity in self.entities.values() if entity.active]

    def get_all_entities_dict(self) -> dict[str, bool]:
        return {name: entity.active for name, entity in self.entities.items()}
    
    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.entities[name].active = active


class BaseClustersTree(ABC):
    def __init__(self, clusters: ClustersHierarchy, prefix: str) -> None:
        self.clusters: ClustersHierarchy = clusters
        self.prefix: str = prefix
        self.clusters_structure: list[str] = []
        self._generate_clusters_structure()

    def _generate_clusters_structure(self) -> None:
        def determine_depth(node: dict[str, Any] | list[str]) -> int:
            if isinstance(node, dict):
                return 1 + max(
                    determine_depth(node=subnode) for subnode in node.values()
                )
            return 0

        depth: int = determine_depth(self.clusters)
        for i in range(depth):
            cluster_name: str = f"{self.prefix}{'Sub' * i}Cluster"
            self.clusters_structure.append(cluster_name)
        self.clusters_structure.append(self.prefix)

    def update_clusters_structure(self, new_structure: ClustersHierarchy) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            entity: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, entities in subclusters.items()
            for entity in entities
        }
        
    @abstractmethod
    def get_clusters_tuples(
        self, entities: list[T]) -> list[tuple[str, ...]]: ...