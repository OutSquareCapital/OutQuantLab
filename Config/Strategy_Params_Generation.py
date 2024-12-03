from typing import List, Dict, Any, Callable, Tuple
from itertools import product
import inspect

def filter_valid_pairs(params: Dict[str, List[int]]) -> List[Dict[str, int]]:
    param_names = list(params.keys())
    param_values = product(*params.values())
    valid_pairs = []

    for values in param_values:
        param_dict = dict(zip(param_names, values))
        if is_valid_combination(param_dict):
            valid_pairs.append(param_dict)

    return valid_pairs

def is_valid_combination(param_dict: Dict[str, int]) -> bool:
    st_param = next((k for k in param_dict if 'ST' in k), None)
    lt_param = next((k for k in param_dict if 'LT' in k), None)
    
    if st_param and lt_param and param_dict[st_param] * 4 > param_dict[lt_param]:
        return False
    
    if 'LenSmooth' in param_dict and 'LenSkew' in param_dict:
        if param_dict['LenSmooth'] > 1 and param_dict['LenSmooth'] * 8 > param_dict['LenSkew']:
            return False

    if 'GroupBy' in param_dict and 'GroupSelected' in param_dict:
        if param_dict['GroupBy'] > 1 and param_dict['GroupSelected'] > 4:
            return False
    
    return True

def determine_array_type(method: Callable) -> str:
    if 'returns_array' in method.__code__.co_varnames:
        return 'returns_array'
    return 'prices_array'

def generate_all_indicators_params(
    methods: List[Callable], 
    options_by_method: Dict[str, Any]
) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
    all_indicators_params = {}
    
    for method in methods:
        method_name = method.__name__  # Utilisation directe du nom de la méthode
        formatted_method_name = ''.join([word.title() for word in method_name.split('_')])

        # Déterminer le type d'entrée
        array_type = determine_array_type(method)
        
        # Extraire les paramètres valides pour la méthode
        method_params = options_by_method.get(method_name, {})
        params = filter_valid_pairs(method_params) if method_params else []

        # Clé finale
        key = f"{formatted_method_name}"
        all_indicators_params[key] = (method, array_type, params)

    return all_indicators_params

def automatic_generation(
    methods: List[Callable], 
    param_options: Dict[str, Any], 
    methods_config: Dict[str, bool]
) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
    # Étape 1 : Filtrer les méthodes actives uniquement
    active_methods = [
        method for method in methods if methods_config.get(method.__name__, False)
    ]

    # Étape 2 : Extraire les options par méthode
    options_by_method = {
        method.__name__: param_options.get(method.__name__, {}) for method in active_methods
    }

    # Étape 3 : Générer les paramètres
    return generate_all_indicators_params(active_methods, options_by_method)