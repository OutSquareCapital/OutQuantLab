from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Tuple
from Files import INDICATORS_PARAMS_FILE, INDICATORS_TO_TEST_FILE, INDICATORS_CLUSTERS_FILE, INDICATORS_MODULE, ASSETS_TO_TEST_CONFIG_FILE, ASSETS_CLUSTERS_FILE, FILE_PATH_YF
from .Config_Funcs import load_config_file, save_config_file, load_asset_names, get_all_indicators_from_module, analyze_indicator_function, filter_valid_pairs
from abc import ABC, abstractmethod

@dataclass
class BaseEntity:
    name: str
    active: bool

@dataclass
class Indicator(BaseEntity):
    func: Callable
    array_type: str
    params: Dict[str, List[int]] = field(default_factory=dict)

class BaseCollection(ABC):

    def __init__(self, entities_file: str, clusters_file: str, primary_keys_file: str):
        self.entities_file = entities_file
        self.clusters_file = clusters_file
        self.primary_keys_file = primary_keys_file
        self.entities: Dict[str, BaseEntity] = {}
        self.clusters = load_config_file(self.clusters_file)
        self._load_entities()

    @abstractmethod
    def _load_entities(self):
        pass
    
    def get_all_entities_names(self) -> List[str]:
        return list(self.entities.keys())

    def get_all_entities(self) -> List[BaseEntity]:
        return list(self.entities.values())

    def get_entity(self, name: str) -> BaseEntity:
        return self.entities[name]

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool):
        self.entities[name].active = active

    def get_active_entities(self) -> List[BaseEntity]:
        return [entity for entity in self.entities.values() if entity.active]

    def get_active_entities_names(self) -> List[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    def update_clusters_structure(self, new_structure: Dict[str, Any]):
        self.clusters = new_structure

    def get_attribute_dict(self, attr: str) -> Dict[str, Any]:
        return {name: getattr(entity, attr) for name, entity in self.entities.items()}
    
    def save(self):
        active_entities = self.get_attribute_dict("active")
        save_config_file(self.entities_file, active_entities, indent=3)
        save_config_file(self.clusters_file, self.clusters, indent=3)

class IndicatorsCollection(BaseCollection):
    def __init__(self):
        super().__init__(INDICATORS_TO_TEST_FILE, INDICATORS_CLUSTERS_FILE, INDICATORS_MODULE)

    def _load_entities(self):
        entities_to_test = load_config_file(self.entities_file)
        params_config = load_config_file(INDICATORS_PARAMS_FILE)
        entities_functions: Dict[str, Callable] = get_all_indicators_from_module(self.primary_keys_file)

        for name, func in entities_functions.items():
            active = entities_to_test.get(name, False)
            array_type, detected_params = analyze_indicator_function(func)
            params = params_config.get(name, {})
            params.update({k: v for k, v in detected_params.items() if k not in params})
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

    def get_params(self, name: str) -> Dict[str, List[int]]:
        return self.entities[name].params

    def set_params(self, name: str, new_params: Dict[str, List[int]]):
        self.entities[name].params = new_params

    def update_param_values(self, name: str, param_key: str, values: List[int]):
        self.entities[name].params[param_key] = values

    def _get_valid_parameter_combinations_for_indicator(self, indicator_name: str) -> List[Dict[str, int]]:
        indicator = self.get_entity(indicator_name)
        if indicator.params:
            return filter_valid_pairs(indicator.params)
        return []

    def get_indicators_and_parameters_for_backtest(self) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
        result = {}
        for indicator in self.get_active_entities():
            formatted_indicator_name = ''.join([word.title() for word in indicator.name.split('_')])
            valid_pairs = self._get_valid_parameter_combinations_for_indicator(indicator.name)
            result[formatted_indicator_name] = (indicator.func, indicator.array_type, valid_pairs)
        return result
    
class AssetsCollection(BaseCollection):
    def __init__(self):
        super().__init__(ASSETS_TO_TEST_CONFIG_FILE, ASSETS_CLUSTERS_FILE, FILE_PATH_YF)

    def _load_entities(self):
        entities_to_test = load_config_file(self.entities_file)
        entities_names = load_asset_names(self.primary_keys_file)
        for name in entities_names:
            is_active = entities_to_test.get(name, False)
            self.entities[name] = BaseEntity(name=name, active=is_active)