import json
from typing import List, Callable, Dict, Any
import inspect
import numpy as np
import importlib
from .Strategy_Params_Generation import automatic_generation

def load_config_file(file_path:str):
    with open(file_path, "r") as file:
        return json.load(file)

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

def get_all_methods_with_args_from_module(module_name: str) -> Dict[str, Dict[str, Any]]:

    module = importlib.import_module(module_name)

    methods_with_args = {}
    for name, func in vars(module).items():
        if callable(func):
            signature = inspect.signature(func)
            args = {
                param_name: param.default if param.default is not inspect.Parameter.empty else None
                for param_name, param in signature.parameters.items()
                if param_name not in ['returns_array', 'prices_array']
            }
            methods_with_args[name] = {
                "function": func,
                "args": args
            }
    
    return methods_with_args

def filter_active_methods(
    current_config: dict, 
    all_methods: Dict[str, Callable]
) -> List[Callable]:
    return [
        all_methods[method_name] for method_name, is_checked in current_config.items() 
        if is_checked and method_name in all_methods
    ]

def dynamic_config(all_methods, methods_to_test, param_config):

    active_methods = filter_active_methods(methods_to_test, all_methods)
    return automatic_generation(active_methods, param_config, methods_to_test)





def sync_methods_with_file(config_file, methods_list: List[str]) -> Dict[str, bool]:

    try:
        # Charger le fichier JSON
        config = load_config_file(config_file)
        if config is None:
            config = {}
    except FileNotFoundError:
        config = {}

    # Synchroniser les méthodes
    updated_config = {method: config.get(method, False) for method in methods_list}

    # Sauvegarder le fichier mis à jour
    save_config_file(config_file, updated_config, 4)
    return updated_config

def sync_with_json(config_file, methods_with_params: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, list]]:

    try:
        # Charger la configuration existante
        existing_config = load_config_file(config_file) or {}
    except FileNotFoundError:
        existing_config = {}

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
