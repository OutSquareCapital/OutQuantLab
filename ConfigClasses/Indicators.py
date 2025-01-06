from Indicators import IndicatorsMethods, IndicatorMetadata
from itertools import product
from Utilitary import IndicatorFunc
from dataclasses import dataclass, field

@dataclass(slots=True)
class Indicator:
    name: str
    active: bool
    func: IndicatorFunc
    params_values: dict[str, list[int]]
    param_combos: list[tuple[int, ...]] = field(default_factory=list)
    strategies_nb: int = 0

class IndicatorsCollection:

    def __init__(self, indicators_to_test: dict[str, bool], params_config: dict[str, dict[str, list[int]]]) -> None:
        self.indicators_to_test: dict[str, bool] = indicators_to_test
        self.params_config: dict[str, dict[str, list[int]]] = params_config
        self.entities: dict[str, Indicator] = {}
        self.load_entities()

    def load_entities(self) -> None: 
        entities_functions: dict[str, IndicatorMetadata] = IndicatorsMethods.get_all_indicators()

        for name, indicator_meta_data in entities_functions.items():
            active: bool = self.indicators_to_test.get(name, False)
            params: dict[str, list[int]] = IndicatorsMethods.determine_params(name=name, params_config=self.params_config)
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

    def filter_valid_pairs(self, params: dict[str, list[int]]) -> list[tuple[int, ...]]:
        parameter_names = list(params.keys())
        parameter_values_combinations = product(*params.values())
        valid_pairs: list[tuple[int, ...]] = []

        for combination in parameter_values_combinations:
            combination_dict = dict(zip(parameter_names, combination))
            if self.is_valid_combination(parameters_dict=combination_dict):
                valid_pairs.append(combination)

        return valid_pairs


    @property
    def indicators_params(self) -> list[Indicator]:
        for indicator in self.all_active_entities:
            indicator.param_combos = self.filter_valid_pairs(params=indicator.params_values)
            indicator.strategies_nb = len(indicator.param_combos)
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
    
    @property
    def all_active_entities_dict(self) -> dict[str, bool]:
        return {name: entity.active for name, entity in self.entities.items()}

    @property
    def all_params_config(self) -> dict[str, dict[str, list[int]]]:
        return {name: indicator.params_values for name, indicator in self.entities.items()}

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
