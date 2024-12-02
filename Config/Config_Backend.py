import json
from Files import ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE, METHODS_CONFIG_FILE
from typing import List, Callable, Dict
import numpy as np
import importlib
from .Strategy_Params_Generation import automatic_generation

def load_config_file(file_path:str):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("define new config, saved file corrupted")

def save_config_file(file_path:str, dict_to_save: dict, indent: int):
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def param_range_values(start: int, end: int, num_values: int, linear: bool = False) -> list:
    if num_values == 1:
        return [int((start + end) / 2)]
    if linear:
        return list(map(int, np.linspace(start, end, num_values)))
    ratio = (end / start) ** (1 / (num_values - 1))
    return [int(round(start * (ratio ** i))) for i in range(num_values)]

def get_all_methods_from_module(module_name: str) -> Dict[str, Callable]:
        
    module = importlib.import_module(module_name)

    return {
        name: func for name, func in vars(module).items() if callable(func)
    }

def filter_active_methods(
    current_config: dict, 
    all_methods: Dict[str, Callable]
) -> List[Callable]:
    
    active_methods = []
    
    for category, methods in current_config.items():
        for method_name, is_checked in methods.items():
            if is_checked and method_name in all_methods:
                method_ref = all_methods[method_name]
                method_ref.__name__ = f"{category}.{method_name}"
                active_methods.append(method_ref)
    
    return active_methods

def dynamic_config(all_methods):
    param_config = load_config_file(PARAM_CONFIG_FILE)
    asset_config = load_config_file(ASSETS_TO_TEST_CONFIG_FILE)
    methods_config = load_config_file(METHODS_CONFIG_FILE)
    active_methods = filter_active_methods(methods_config, all_methods)
    indicators_and_params = automatic_generation(active_methods, param_config, methods_config)
    return indicators_and_params, asset_config