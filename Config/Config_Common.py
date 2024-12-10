import json
import pyarrow.parquet as pq
from typing import Dict, List, Callable, Tuple
import importlib
from inspect import signature

def load_config_file(file_path: str) -> dict:
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
