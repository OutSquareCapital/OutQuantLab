import json
import pyarrow.parquet as pq
from typing import Dict, List, Callable, Tuple, Any
import importlib
from inspect import signature
from itertools import product

def load_config_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path: str, dict_to_save: dict, indent: int):
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def load_asset_names(file_path: str) -> List[str]:
    column_names = pq.ParquetFile(file_path).schema.names
    return [col for col in column_names if col != "Date"]

def get_all_indicators_from_module(module_name: str) -> Dict[str, Callable]:
    module = importlib.import_module(module_name)
    return {
        name: func for name, func in vars(module).items() if callable(func)
    }

def analyze_indicator_function(func: Callable) -> Tuple[str, Dict[str, List[int]]]:

    array_type = 'returns_array' if 'returns_array' in func.__code__.co_varnames else 'prices_array'
    excluded_params = {'returns_array', 'prices_array'}
    func_signature = signature(func)
    params = {param_name: [] for param_name in func_signature.parameters.keys() if param_name not in excluded_params}

    return array_type, params

def is_valid_combination(parameters_dict: Dict[str, int]) -> bool:
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

def filter_valid_pairs(params: Dict[str, List[int]]) -> List[Dict[str, int]]:
    parameter_names = list(params.keys())
    parameter_values_combinations = product(*params.values())
    valid_pairs = []

    for combination in parameter_values_combinations:
        combination_dict = dict(zip(parameter_names, combination))
        if is_valid_combination(combination_dict):
            valid_pairs.append(combination_dict)

    return valid_pairs