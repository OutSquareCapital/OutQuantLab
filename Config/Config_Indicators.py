from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Tuple
from Files import INDICATORS_PARAMS_FILE, INDICATORS_TO_TEST_FILE, INDICATORS_CLUSTERS_FILE
from .Config_Common import load_config_file, save_config_file, get_all_indicators_from_module, analyze_indicator_function
from itertools import product

@dataclass
class Indicator:
    name: str
    active: bool
    func: Callable
    array_type: str
    params: Dict[str, List[int]] = field(default_factory=dict)

class IndicatorsCollection:
    def __init__(self, indicators_module: str = 'Signals'):
        self.indicators_module: str = indicators_module
        self._indicators: Dict[str, Indicator] = {}
        self.clusters: Dict[str, Any] = {}
        self._load()

    def _load(self):
        indicators_to_test = load_config_file(INDICATORS_TO_TEST_FILE)  # {indicator_name: bool}
        params_config = load_config_file(INDICATORS_PARAMS_FILE)  # {indicator_name: {param_name: [values]}}
        self.clusters = load_config_file(INDICATORS_CLUSTERS_FILE)  # dict représentant la structure des clusters

        indicators_functions: Dict[str, Callable] = get_all_indicators_from_module(self.indicators_module)

        for indicator_name, func in indicators_functions.items():
            active = indicators_to_test.get(indicator_name, False)

            array_type, detected_params = analyze_indicator_function(func)

            params = params_config.get(indicator_name, {})
            
            params.update({k: v for k, v in detected_params.items() if k not in params})

            self._indicators[indicator_name] = Indicator(
                name=indicator_name,
                active=active,
                func=func,
                array_type=array_type,
                params=params
            )

    def get_all_objects_names(self) -> List[str]:
        return list(self._indicators.keys())

    def get_all_objects(self) -> List[Indicator]:
        return list(self._indicators.values())

    def get_object(self, name: str) -> Indicator:
        return self._indicators[name]

    def is_active(self, name: str) -> bool:
        return self._indicators[name].active

    def set_active(self, name: str, active: bool):
        self._indicators[name].active = active

    def get_params(self, name: str) -> Dict[str, List[int]]:
        return self._indicators[name].params

    def set_params(self, name: str, new_params: Dict[str, List[int]]):
        self._indicators[name].params = new_params

    def update_param_values(self, name: str, param_key: str, values: List[int]):
        self._indicators[name].params[param_key] = values

    def get_active_indicators(self) -> List[Indicator]:
        return [indicator for indicator in self._indicators.values() if indicator.active]

    def update_clusters_structure(self, new_structure: Dict[str, Any]):
        self.clusters = new_structure

    def _is_valid_combination(self, parameters_dict: Dict[str, int]) -> bool:
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

    def _filter_valid_pairs(self, params: Dict[str, List[int]]) -> List[Dict[str, int]]:
        parameter_names = list(params.keys())
        parameter_values_combinations = product(*params.values())
        valid_pairs = []

        for combination in parameter_values_combinations:
            combination_dict = dict(zip(parameter_names, combination))
            if self._is_valid_combination(combination_dict):
                valid_pairs.append(combination_dict)

        return valid_pairs

    def _get_valid_parameter_combinations_for_indicator(self, indicator_name: str) -> List[Dict[str, int]]:
        indicator = self.get_object(indicator_name)
        if indicator.params:
            return self._filter_valid_pairs(indicator.params)
        return []

    def get_indicators_and_parameters_for_backtest(self) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
        result = {}
        for indicator in self.get_active_indicators():
            formatted_indicator_name = ''.join([word.title() for word in indicator.name.split('_')])
            valid_pairs = self._get_valid_parameter_combinations_for_indicator(indicator.name)
            result[formatted_indicator_name] = (indicator.func, indicator.array_type, valid_pairs)
        return result

    def save(self):
        parameters_to_save = {indicator_name: indicator.params for indicator_name, indicator in self._indicators.items()}
        indicators_active_config = {indicator_name: indicator.active for indicator_name, indicator in self._indicators.items()}

        save_config_file(INDICATORS_PARAMS_FILE, parameters_to_save, indent=3)
        save_config_file(INDICATORS_TO_TEST_FILE, indicators_active_config, indent=3)
        save_config_file(INDICATORS_CLUSTERS_FILE, self.clusters, indent=3)