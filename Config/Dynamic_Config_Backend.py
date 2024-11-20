import json
from Config import assets_to_backtest, DYNAMIC_CONFIG_FILE
from typing import Dict, List

def save_last_config(config: Dict[str, List[str]]):
    with open(DYNAMIC_CONFIG_FILE, "w") as file:
        json.dump(config, file)

def load_last_config_on_launch():
    try:
        with open(DYNAMIC_CONFIG_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("define new config, saved file corrupted")