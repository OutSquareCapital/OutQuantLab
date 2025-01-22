from typing import Protocol, TypeVar, Generic, Any
from abc import ABC, abstractmethod

class StrategyComponent(Protocol):
    name: str
    active: bool

T = TypeVar("T", bound=StrategyComponent)

class BaseCollection(ABC, Generic[T]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.entities: dict[str, T] = {} 
        self._load_entities(*args, **kwargs)

    @abstractmethod
    def _load_entities(self, *args: Any, **kwargs: Any) -> None: ...

    @property
    def all_entities_names(self) -> list[str]:
        return list(self.entities.keys())

    @property
    def all_entities(self) -> list[T]:
        return list(self.entities.values())

    @property
    def all_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    @property
    def all_active_entities(self) -> list[T]:
        return [entity for entity in self.entities.values() if entity.active]

    @property
    def all_active_entities_dict(self) -> dict[str, bool]:
        return {name: entity.active for name, entity in self.entities.items()}

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.entities[name].active = active
