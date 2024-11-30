import json
from Files import ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE, METHODS_CONFIG_FILE
from typing import Dict, List, Callable
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

def get_active_methods(current_config: dict, module_name: str = "Signals.Signals_Normalized") -> List[Callable]:
    active_methods = []
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return []

    for category, methods in current_config.items():
        cls = getattr(module, category, None)
        if cls is None:
            continue

        for method, is_checked in methods.items():
            if is_checked:
                method_ref = getattr(cls, method, None)
                if callable(method_ref):
                    active_methods.append(method_ref)
    return active_methods

def dynamic_config():
    param_config = load_config_file(PARAM_CONFIG_FILE)
    asset_config = load_config_file(ASSETS_TO_TEST_CONFIG_FILE)
    methods_config = load_config_file(METHODS_CONFIG_FILE)
    active_methods = get_active_methods(methods_config)
    indicators_and_params = automatic_generation(active_methods, param_config)
    return indicators_and_params, asset_config
