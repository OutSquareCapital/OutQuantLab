from dataclasses import dataclass, field
from typing import Any, TypeVar, Generic
from types import MappingProxyType
from Files import INDICATORS_PARAMS_FILE, INDICATORS_TO_TEST_FILE, INDICATORS_CLUSTERS_FILE, INDICATORS_MODULE, ASSETS_TO_TEST_CONFIG_FILE, ASSETS_CLUSTERS_FILE, FILE_PATH_YF
from .Config_Funcs import load_config_file, save_config_file, load_asset_names, get_all_indicators_from_module, determine_indicator_params, filter_valid_pairs, determine_array_type
from abc import ABC, abstractmethod
from collections.abc import Callable
from inspect import signature, Parameter

@dataclass
class BaseEntity(ABC):
    name: str
    active: bool

@dataclass
class Asset(BaseEntity):
    category: str

@dataclass
class Indicator(BaseEntity):
    func: Callable
    array_type: str
    params: dict[str, list[int]] = field(default_factory=dict)

T = TypeVar("T", bound=BaseEntity)

class BaseCollection(Generic[T]):

    def __init__(self, entities_file: str, clusters_file: str, primary_keys_file: str):
        self.entities_file: str = entities_file
        self.clusters_file: str = clusters_file
        self.primary_keys_file: str = primary_keys_file
        self.entities: dict[str, T] = {}
        self.clusters = load_config_file(self.clusters_file)
        self._load_entities()

    @abstractmethod
    def _load_entities(self):
        pass
    
    def get_all_entities_names(self) -> list[str]:
        return list(self.entities.keys())

    def get_all_entities(self) -> list[T]:
        return list(self.entities.values())

    def get_entity(self, name: str) -> T:
        return self.entities[name]

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool):
        self.entities[name].active = active

    def get_active_entities(self) -> list[T]:
        return [entity for entity in self.entities.values() if entity.active]

    def get_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    def update_clusters_structure(self, new_structure: dict[str, Any]):
        self.clusters = new_structure

    def get_attribute_dict(self, attr: str) -> dict[str, Any]:
        return {name: getattr(entity, attr) for name, entity in self.entities.items()}
    
    def save(self):
        active_entities = self.get_attribute_dict("active")
        save_config_file(self.entities_file, active_entities, indent=3)
        save_config_file(self.clusters_file, self.clusters, indent=3)

class IndicatorsCollection(BaseCollection[Indicator]):
    def __init__(self):
        super().__init__(INDICATORS_TO_TEST_FILE, INDICATORS_CLUSTERS_FILE, INDICATORS_MODULE)

    def _load_entities(self):
        entities_to_test: dict[str, bool] = load_config_file(self.entities_file)
        entities_functions: dict[str, Callable] = get_all_indicators_from_module(self.primary_keys_file)
        params_config: dict[str, dict[str, list[int]]] = load_config_file(INDICATORS_PARAMS_FILE)

        for name, func in entities_functions.items():
            func_signature: MappingProxyType[str, Parameter] = signature(func).parameters
            active: bool = entities_to_test.get(name, False)
            array_type: str = determine_array_type(func_signature)
            params: dict[str, list[int]] = determine_indicator_params(func_signature, name, params_config, array_type)
            
            self.entities[name] = Indicator(
                name=name,
                active=active,
                func=func,
                array_type=array_type,
                params=params
            )

    def save(self):
        super().save()
        parameters_to_save = self.get_attribute_dict("params")
        save_config_file(INDICATORS_PARAMS_FILE, parameters_to_save, indent=3)

    def get_params(self, name: str) -> dict[str, list[int]]:
        return self.entities[name].params

    def set_params(self, name: str, new_params: dict[str, list[int]]):
        self.entities[name].params = new_params

    def update_param_values(self, name: str, param_key: str, values: list[int]):
        self.entities[name].params[param_key] = values

    def get_indicators_and_parameters_for_backtest(self) -> dict[str, tuple[Callable, str, list[dict[str, int]]]]:

        result = {}
        for indicator in self.get_active_entities():
            formatted_indicator_name = ''.join([word.title() for word in indicator.name.split('_')])
            valid_pairs =  filter_valid_pairs(indicator.params)
            result[formatted_indicator_name] = (indicator.func, indicator.array_type, valid_pairs)
        return result
    
class AssetsCollection(BaseCollection[Asset]):
    def __init__(self):
        super().__init__(ASSETS_TO_TEST_CONFIG_FILE, ASSETS_CLUSTERS_FILE, FILE_PATH_YF)

    def _load_entities(self):
        entities_to_test = load_config_file(self.entities_file)
        entities_names = load_asset_names(self.primary_keys_file)
        for name in entities_names:
            is_active = entities_to_test.get(name, False)
            self.entities[name] = Asset(
                name=name, 
                active=is_active,
                category=''
                )