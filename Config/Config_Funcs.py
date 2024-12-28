from itertools import product

def is_valid_combination(parameters_dict: dict[str, int]) -> bool:
    short_term_param = next((k for k in parameters_dict if 'ST' in k), None)
    long_term_param = next((k for k in parameters_dict if 'LT' in k), None)
    
    if short_term_param and long_term_param:
        if parameters_dict[short_term_param] * 4 > parameters_dict[long_term_param]:
            return False

    if 'LenSmooth' in parameters_dict and 'LenSkew' in parameters_dict:
        if parameters_dict['LenSmooth'] > 1 and parameters_dict['LenSmooth'] * 8 > parameters_dict['LenSkew']:
            return False

    if 'GroupBy' in parameters_dict and 'GroupSelected' in parameters_dict:
        if parameters_dict['GroupBy'] > 1 and parameters_dict['GroupSelected'] > 4:
            return False

    return True

def filter_valid_pairs(params: dict[str, list[int]]) -> list[dict[str, int]]:
    parameter_names = list(params.keys())
    parameter_values_combinations = product(*params.values())
    valid_pairs: list[dict[str, int]] = []

    for combination in parameter_values_combinations:
        combination_dict = dict(zip(parameter_names, combination))
        if is_valid_combination(combination_dict):
            valid_pairs.append(combination_dict)

    return valid_pairs
