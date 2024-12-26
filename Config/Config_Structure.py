from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

from Files import (
INDICATORS_PARAMS_FILE, 
INDICATORS_TO_TEST_FILE, 
INDICATORS_MODULE, 
ASSETS_TO_TEST_CONFIG_FILE, 
FILE_PATH_YF,
IndicatorFunc
)
from .Config_Funcs import (
load_config_file, 
save_config_file,
load_asset_names,
filter_valid_pairs
)

from Indicators import IndicatorsMethods

@dataclass(slots=True)
class IndicatorParams:
    name: str
    func: IndicatorFunc
    param_combos: list[dict[str, int]]

@dataclass
class BaseEntity(ABC):
    name: str
    active: bool

@dataclass
class Asset(BaseEntity):
    category: str

@dataclass
class Indicator(BaseEntity):
    func: IndicatorFunc
    params: dict[str, list[int]] = field(default_factory=dict)

T = TypeVar("T", bound=BaseEntity)

class ClustersTree:
    def __init__(self, clusters_file: str) -> None:
        self.clusters_file: str = clusters_file
        self.clusters = load_config_file(self.clusters_file)

    def update_clusters_structure(self, new_structure: dict[str, Any]) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_assets(self) -> dict[str, tuple[str, str]]:
        return {
            asset: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, assets in subclusters.items()
            for asset in assets
        }

    def save(self) -> None:
        save_config_file(self.clusters_file, self.clusters, indent=3)

class BaseCollection(Generic[T]):

    def __init__(self, entities_file: str, primary_keys_file: str) -> None:
        self.entities_file: str = entities_file
        self.primary_keys_file: str = primary_keys_file
        self.entities: dict[str, T] = {}
        self._load_entities()

    @abstractmethod
    def _load_entities(self) -> None:
        pass

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

    def get_entity(self, name: str) -> T:
        return self.entities[name]

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.entities[name].active = active

    def save(self) -> None:
        active_entities = {name: entity.active for name, entity in self.entities.items()}
        save_config_file(self.entities_file, active_entities, indent=3)

class IndicatorsCollection(BaseCollection[Indicator]):
    def __init__(self) -> None:
        super().__init__(INDICATORS_TO_TEST_FILE, INDICATORS_MODULE)

    def _load_entities(self) -> None:
        indics_methods = IndicatorsMethods()
        entities_to_test: dict[str, bool] = load_config_file(self.entities_file)
        entities_functions: dict[str, IndicatorFunc] = indics_methods.get_all_signals()
        params_config: dict[str, dict[str, list[int]]] = load_config_file(INDICATORS_PARAMS_FILE)

        for name, func in entities_functions.items():
            active: bool = entities_to_test.get(name, False)
            params: dict[str, list[int]] = indics_methods.determine_params(name, params_config)
            self.entities[name] = Indicator(
                name=name,
                active=active,
                func=func,
                params=params
            )

    @property
    def indicators_params_dict(self) -> list[IndicatorParams]:
        result: list[IndicatorParams] = []
        for indicator in self.all_active_entities:
            valid_pairs = filter_valid_pairs(indicator.params)
            result.append(IndicatorParams(
                name=indicator.name,
                func=indicator.func,
                param_combos=valid_pairs
            ))
        return result

    def save(self) -> None:
        super().save()
        parameters_to_save = {name: indicator.params for name, indicator in self.entities.items()}
        save_config_file(INDICATORS_PARAMS_FILE, parameters_to_save, indent=3)

    def get_params(self, name: str) -> dict[str, list[int]]:
        return self.entities[name].params

    def set_params(self, name: str, new_params: dict[str, list[int]]) -> None:
        self.entities[name].params = new_params

    def update_param_values(self, name: str, param_key: str, values: list[int]) -> None:
        self.entities[name].params[param_key] = values
    
class AssetsCollection(BaseCollection[Asset]):
    def __init__(self) -> None:
        super().__init__(ASSETS_TO_TEST_CONFIG_FILE, FILE_PATH_YF)

    def _load_entities(self) -> None:
        entities_to_test = load_config_file(self.entities_file)
        entities_names = load_asset_names(self.primary_keys_file)
        for name in entities_names:
            is_active = entities_to_test.get(name, False)
            self.entities[name] = Asset(
                name=name, 
                active=is_active,
                category=''
                )