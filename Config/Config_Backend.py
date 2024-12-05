import json
from typing import List, Callable, Dict, Any
import importlib
import os
import tempfile
import pyarrow.parquet as pq
from Files import ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE, METHODS_TO_TEST_FILE, ASSETS_CLASSES_FILE, METHODS_CLASSES_FILE

def load_asset_names(file_path: str) -> List[str]:
    parquet_file = pq.ParquetFile(file_path)
    column_names = parquet_file.schema.names
    return [col for col in column_names if col != "Date"]


def get_all_methods_from_module(module_name: str) -> Dict[str, Callable]:
        
    module = importlib.import_module(module_name)

    return {
        name: func for name, func in vars(module).items() if callable(func)
    }

def save_html_temp_file(html_content: str, suffix: str = "outquant.html") -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return temp_file.name

def cleanup_temp_files():
    temp_dir = tempfile.gettempdir()
    for file_name in os.listdir(temp_dir):
        if file_name.endswith("outquant.html"):
            file_path = os.path.join(temp_dir, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier temporaire {file_path} : {e}")

def load_config_file(file_path:str):
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path:str, dict_to_save: dict, indent: int):
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def load_all_json_files() -> Dict[str, Any]:
    return {
        "assets_to_test": load_config_file(ASSETS_TO_TEST_CONFIG_FILE),
        "params_config": load_config_file(PARAM_CONFIG_FILE),
        "methods_to_test": load_config_file(METHODS_TO_TEST_FILE),
        "methods_classes": load_config_file(METHODS_CLASSES_FILE),
        "assets_classes": load_config_file(ASSETS_CLASSES_FILE),
    }

def save_all_json_files(data: Dict[str, Any], indent: int = 4):
    save_config_file(ASSETS_TO_TEST_CONFIG_FILE, data["assets_to_test"], indent)
    save_config_file(PARAM_CONFIG_FILE, data["params_config"], indent)
    save_config_file(METHODS_TO_TEST_FILE, data["methods_to_test"], indent)
    save_config_file(METHODS_CLASSES_FILE, data["methods_classes"], indent)
    save_config_file(ASSETS_CLASSES_FILE, data["assets_classes"], indent)