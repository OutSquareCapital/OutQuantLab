import json
from typing import List, Callable, Dict, Any
import importlib
import os
import tempfile
import pyarrow.parquet as pq

def load_asset_names(file_path: str) -> List[str]:
    parquet_file = pq.ParquetFile(file_path)
    column_names = parquet_file.schema.names
    return [col for col in column_names if col != "Date"]


def load_config_file(file_path:str):
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path:str, dict_to_save: dict, indent: int):
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

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
            
def sync_methods_with_file(config_file, methods_list: List[str]) -> Dict[str, bool]:

    config = load_config_file(config_file)

    # Synchroniser les méthodes
    updated_config = {method: config.get(method, False) for method in methods_list}

    save_config_file(config_file, updated_config, 4)
    return updated_config

def sync_with_json(config_file, methods_with_params: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, list]]:

    existing_config = load_config_file(config_file)

    # Filtrer les méthodes avec leurs arguments, supprimer la clé 'function'
    filtered_methods_with_params = {
        method: params.get("args", {}) for method, params in methods_with_params.items()
    }

    # Mettre à jour la configuration pour correspondre aux méthodes fournies
    updated_config = {}
    for method, params in filtered_methods_with_params.items():
        if method not in existing_config:
            # Nouvelle méthode
            updated_config[method] = {param: values if values else [1] for param, values in params.items()}
        else:
            # Méthode existante, mise à jour des paramètres
            updated_config[method] = {
                param: existing_config[method].get(param, values if values else [1])
                for param, values in params.items()
            }

    # Sauvegarder la configuration mise à jour
    save_config_file(config_file, updated_config, indent=4)
    return updated_config
