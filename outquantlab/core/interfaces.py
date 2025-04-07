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

    def get_all_entities(self) -> list[T]:
        return list(self.entities.values())

    def get_all_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values()]

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
