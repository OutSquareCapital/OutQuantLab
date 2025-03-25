from abc import ABC, abstractmethod
from typing import Any, Protocol


class StrategyComponent(Protocol):
    name: str
    active: bool


class BaseConfig[T: StrategyComponent](ABC):
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


class BaseClustersTree[T: StrategyComponent](ABC):
    def __init__(self, clusters: dict[str, dict[str, list[str]]]) -> None:
        self.clusters: dict[str, dict[str, list[str]]] = clusters

    def update_clusters_structure(
        self, new_structure: dict[str, dict[str, list[str]]]
    ) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            entity: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, entities in subclusters.items()
            for entity in entities
        }

    @abstractmethod
    def get_clusters_tuples(self, entities: list[T]) -> list[tuple[str, ...]]: ...
