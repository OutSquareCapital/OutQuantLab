from Indicators import IndicatorsMethods, IndicatorMetadata
from itertools import product
from Utilitary import IndicatorFunc, JsonData
from dataclasses import dataclass, field
from Database import load_config_file, save_config_file

@dataclass(slots=True)
class Indicator:
    name: str
    active: bool
    func: IndicatorFunc
    param_combos: list[dict[str, int]] = field(default_factory=list)
    params_values: dict[str, list[int]] = field(default_factory=dict)

class IndicatorsCollection:

    def __init__(self, indicators_to_test: JsonData, indicators_params: JsonData) -> None:
        self.entities_file: JsonData = indicators_to_test
        self.params_file: JsonData = indicators_params
        self.entities: dict[str, Indicator] = {}
        self.load_entities()

    def load_entities(self) -> None:
        entities_to_test: dict[str, bool] = load_config_file(self.entities_file)
        entities_functions: dict[str, IndicatorMetadata] = IndicatorsMethods.get_all_indicators()
        params_config: dict[str, dict[str, list[int]]] = load_config_file(self.params_file)

        for name, indicator_meta_data in entities_functions.items():
            active: bool = entities_to_test.get(name, False)
            params: dict[str, list[int]] = IndicatorsMethods.determine_params(name, params_config)
            func = indicator_meta_data.func
            self.entities[name] = Indicator(
                name=name,
                active=active,
                func=func,
                params_values=params
            )

    def is_valid_combination(self, parameters_dict: dict[str, int]) -> bool:
        short_term_param = next((k for k in parameters_dict if 'ST' in k), None)
        long_term_param = next((k for k in parameters_dict if 'LT' in k), None)
        
        if short_term_param and long_term_param:
            if parameters_dict[short_term_param] * 4 > parameters_dict[long_term_param]:
                return False

        if 'LenSmooth' in parameters_dict and 'LenSkew' in parameters_dict:
            if parameters_dict['LenSmooth'] > 1 and parameters_dict['LenSmooth'] * 8 > parameters_dict['LenSkew']:
                return False

        if 'GroupBy' in parameters_dict and 'GroupSelected' in parameters_dict:
            if parameters_dict['GroupBy'] > 1 and parameters_dict['GroupSelected'] > 4:
                return False

        return True

    def filter_valid_pairs(self, params: dict[str, list[int]]) -> list[dict[str, int]]:
        parameter_names = list(params.keys())
        parameter_values_combinations = product(*params.values())
        valid_pairs: list[dict[str, int]] = []

        for combination in parameter_values_combinations:
            combination_dict = dict(zip(parameter_names, combination))
            if self.is_valid_combination(combination_dict):
                valid_pairs.append(combination_dict)

        return valid_pairs

    @property
    def indicators_params(self) -> list[Indicator]:
        for indicator in self.all_active_entities:
            indicator.param_combos = self.filter_valid_pairs(indicator.params_values)
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
