import json
from numpy.typing import NDArray
import pyarrow.parquet as pq # type: ignore
from types import MappingProxyType
from typing import Any
from collections.abc import Callable
import importlib
from itertools import product
from inspect import Parameter
from numpy.typing import NDArray
import numpy as np

def load_config_file(file_path: str) -> dict[str, Any]:
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path: str, dict_to_save: dict[str, Any], indent: int) -> None:
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def load_asset_names(file_path: str) -> list[str]:
    column_names: list[str] = pq.ParquetFile(file_path).schema.names # type: ignore
    return [col for col in column_names if col != "Date"] # type: ignore

def get_all_indicators_from_module(module_name: str) -> dict[str, Callable[..., NDArray[np.float32]]]:
    module = importlib.import_module(module_name)
    indicators = vars(module).items()

    formatted_indicators: dict[str, Callable[..., NDArray[np.float32]]] = {}
    for name, func in indicators:
        if callable(func):
            formatted_name:str = ''.join(word.title() for word in name.split('_'))
            formatted_indicators[formatted_name] = func # type: ignore

    return formatted_indicators

def determine_array_type(func_params: MappingProxyType[str, Parameter]) -> str:
    return 'returns_array' if 'returns_array' in func_params else 'prices_array'

def determine_indicator_params(
    func_signature: MappingProxyType[str, Parameter],
    name: str,
    params_config: dict[str, dict[str, list[int]]],
    array_type: str
) -> dict[str, list[int]]:
    
    param_values = params_config.get(name, {})
    return {
        param_name: param_values.get(param_name, [])
        for param_name in func_signature.keys()
        if param_name != array_type
    }

def is_valid_combination(parameters_dict: dict[str, int]) -> bool:
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

def filter_valid_pairs(params: dict[str, list[int]]) -> list[dict[str, int]]:
    parameter_names = list(params.keys())
    parameter_values_combinations = product(*params.values())
    valid_pairs: list[dict[str, int]] = []

    for combination in parameter_values_combinations:
        combination_dict = dict(zip(parameter_names, combination))
        if is_valid_combination(combination_dict):
            valid_pairs.append(combination_dict)

    return valid_pairs
