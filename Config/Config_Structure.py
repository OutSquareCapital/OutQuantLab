from dataclasses import dataclass, field
from typing import Any
from Files import IndicatorFunc
from .Config_Funcs import (
load_config_file, 
save_config_file,
load_asset_names,
filter_valid_pairs
)
from Indicators import IndicatorsMethods

class ClustersTree:
    def __init__(self, clusters_file: str) -> None:
        self.clusters_file: str = clusters_file
        self.clusters = load_config_file(self.clusters_file)

    def update_clusters_structure(self, new_structure: dict[str, Any]) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            asset: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, assets in subclusters.items()
            for asset in assets
        }

    def save(self) -> None:
        save_config_file(self.clusters_file, self.clusters, indent=3)

@dataclass(slots=True)
class Indicator:
    name: str
    active: bool
    func: IndicatorFunc
    param_combos: list[dict[str, int]] = field(default_factory=list)
    params_values: dict[str, list[int]] = field(default_factory=dict)

class IndicatorsCollection:

    def __init__(self, indicators_to_test, indicators_params) -> None:
        self.entities_file: str = indicators_to_test
        self.params_file: str = indicators_params
        self.entities: dict[str, Indicator] = {}
        self.load_entities()

    def load_entities(self) -> None:
        entities_to_test: dict[str, bool] = load_config_file(self.entities_file)
        entities_functions: dict[str, IndicatorFunc] = IndicatorsMethods.get_all_indicators()
        params_config: dict[str, dict[str, list[int]]] = load_config_file(self.params_file)

        for name, func in entities_functions.items():
            active: bool = entities_to_test.get(name, False)
            params: dict[str, list[int]] = IndicatorsMethods.determine_params(name, params_config)
            self.entities[name] = Indicator(
                name=name,
                active=active,
                func=func,
                params_values=params
            )

    @property
    def indicators_params(self) -> list[Indicator]:
        for indicator in self.all_active_entities:
            indicator.param_combos = filter_valid_pairs(indicator.params_values)
        return self.all_active_entities

    @property
    def all_entities_names(self) -> list[str]:
        return list(self.entities.keys())

    @property
    def all_entities(self) -> list[Indicator]:
        return list(self.entities.values())

    @property
    def all_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    @property
    def all_active_entities(self) -> list[Indicator]:
        return [entity for entity in self.entities.values() if entity.active]

    def get_entity(self, name: str) -> Indicator:
        return self.entities[name]

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.entities[name].active = active

    def get_params(self, name: str) -> dict[str, list[int]]:
        return self.entities[name].params_values

    def set_params(self, name: str, new_params: dict[str, list[int]]) -> None:
        self.entities[name].params_values = new_params

    def update_param_values(self, name: str, param_key: str, values: list[int]) -> None:
        self.entities[name].params_values[param_key] = values

    def save(self) -> None:
        active_entities = {name: entity.active for name, entity in self.entities.items()}
        save_config_file(self.entities_file, active_entities, indent=3)
        parameters_to_save = {name: indicator.params_values for name, indicator in self.entities.items()}
        save_config_file(self.params_file, parameters_to_save, indent=3)

@dataclass(slots=True)
class Asset:
    name: str
    active: bool
    category: str

class AssetsCollection:
    def __init__(self, assets_to_test, assets_data) -> None:
        self.entities_file: str = assets_to_test
        self.primary_keys_file: str = assets_data
        self.entities: dict[str, Asset] = {}
        self.load_entities()

    def load_entities(self) -> None:
        entities_to_test = load_config_file(self.entities_file)
        entities_names = load_asset_names(self.primary_keys_file)
        for name in entities_names:
            is_active = entities_to_test.get(name, False)
            self.entities[name] = Asset(
                name=name, 
                active=is_active,
                category=''
                )

    @property
    def all_entities_names(self) -> list[str]:
        return list(self.entities.keys())

    @property
    def all_entities(self) -> list[Asset]:
        return list(self.entities.values())

    @property
    def all_active_entities_names(self) -> list[str]:
        return [entity.name for entity in self.entities.values() if entity.active]

    @property
    def all_active_entities(self) -> list[Asset]:
        return [entity for entity in self.entities.values() if entity.active]

    def get_entity(self, name: str) -> Asset:
        return self.entities[name]

    def is_active(self, name: str) -> bool:
        return self.entities[name].active

    def set_active(self, name: str, active: bool) -> None:
        self.entities[name].active = active

    def save(self) -> None:
        active_entities = {name: entity.active for name, entity in self.entities.items()}
        save_config_file(self.entities_file, active_entities, indent=3)