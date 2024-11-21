import json
from Config import ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE, METHODS_CONFIG_FILE
from typing import Dict, List, Callable
import numpy as np
import importlib

def load_assets_to_backtest_config():
    try:
        with open(ASSETS_TO_TEST_CONFIG_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("define new config, saved file corrupted")

def save_assets_to_backtest_config(config: Dict[str, List[str]]):
    with open(ASSETS_TO_TEST_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=3)

def load_param_config() -> dict:
    try:
        with open(PARAM_CONFIG_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError):
        print("define new config, saved file corrupted")

def save_param_config(config: dict):
    with open(PARAM_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def load_methods_config() -> Dict[str, Dict[str, bool]]:

    try:
        with open(METHODS_CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("define new config, saved file corrupted")
        return {}

def save_methods_config(config: Dict[str, Dict[str, bool]]) -> None:

    with open(METHODS_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

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