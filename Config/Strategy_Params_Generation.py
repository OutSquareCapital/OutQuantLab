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

def extract_class_and_method_names(method: Callable) -> Tuple[str, str]:
    method_str = str(method)
    class_name, method_name = method_str.split()[1].split('.')
    return class_name, method_name


def extract_options_by_class(
    methods: List[Callable], 
    param_options: Dict[str, Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    options_by_class = {}
    
    for method in methods:
        # Extraire la catégorie depuis le paramètre
        class_name = method.__name__.split('.')[0]  # La catégorie est ajoutée dans `get_active_methods`
        if class_name not in options_by_class:
            options_by_class[class_name] = {}

        # Obtenir les paramètres de la méthode
        params = inspect.signature(method).parameters
        for param in params:
            if param not in ['returns_array', 'prices_array']:
                param_option = param_options.get(class_name, {}).get(param, None)
                if param_option is not None:
                    options_by_class[class_name].setdefault(param, param_option)

    return options_by_class

def determine_array_type(method: Callable) -> str:
    if 'returns_array' in method.__code__.co_varnames:
        return 'returns_array'
    return 'prices_array'

def generate_all_indicators_params(
    methods: List[Callable], 
    options_by_class: Dict[str, Dict[str, Any]], 
    method_to_category: Dict[Callable, str]
) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
    all_indicators_params = {}
    
    for method in methods:
        # Obtenir la catégorie de la méthode
        class_name = method_to_category.get(method)
        if not class_name:
            continue
        
        method_name = method.__name__.split('.')[-1]  # Extraire le vrai nom
        formatted_method_name = ''.join([word.title() for word in method_name.split('_')])

        # Déterminer le type d'entrée
        array_type = determine_array_type(method)
        
        # Extraire les paramètres valides pour la catégorie
        class_params = options_by_class.get(class_name, {})
        params = filter_valid_pairs(class_params) if class_params else []

        # Clé finale
        key = f"{class_name}_{formatted_method_name}"
        all_indicators_params[key] = (method, array_type, params)

    return all_indicators_params

def automatic_generation(
    methods: List[Callable], 
    param_options: Dict[str, Dict[str, Any]], 
    methods_config: Dict[str, Dict[str, bool]]
) -> Dict[str, Tuple[Callable, str, List[Dict[str, int]]]]:
    # Étape 1 : Créer un mapping méthode -> catégorie
    method_to_category = {
        method: category
        for category, methods_dict in methods_config.items()
        for method_name, is_checked in methods_dict.items()
        if is_checked
        for method in methods
        if method.__name__.endswith(method_name)
    }

    # Étape 2 : Extraire les options par catégorie
    options_by_class = extract_options_by_class(methods, param_options)

    # Étape 3 : Générer les paramètres
    return generate_all_indicators_params(methods, options_by_class, method_to_category)
