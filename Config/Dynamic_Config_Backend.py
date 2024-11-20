import json
from Config import DYNAMIC_CONFIG_FILE, PARAM_CONFIG_FILE
from typing import Dict, List
import numpy as np

def load_assets_to_backtest_config():
    try:
        with open(DYNAMIC_CONFIG_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("define new config, saved file corrupted")

def save_assets_to_backtest_config(config: Dict[str, List[str]]):
    with open(DYNAMIC_CONFIG_FILE, "w") as file:
        json.dump(config, file)

def load_param_config() -> dict:
    try:
        with open(PARAM_CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_param_config(config: dict):
    with open(PARAM_CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def param_range_values(start: int, end: int, num_values: int, linear: bool = False) -> list:
    if num_values == 1:
        return [int((start + end) / 2)]
    if linear:
        return list(map(int, np.linspace(start, end, num_values)))
    ratio = (end / start) ** (1 / (num_values - 1))
    return [int(round(start * (ratio ** i))) for i in range(num_values)]