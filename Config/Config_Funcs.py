import json
import pyarrow.parquet as pq # type: ignore
from Utilitary import DictVariableDepth
from itertools import product

def load_config_file(file_path: str) -> DictVariableDepth:
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path: str, dict_to_save: DictVariableDepth, indent: int) -> None:
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def load_asset_names(file_path: str) -> list[str]:
    column_names: list[str] = pq.ParquetFile(file_path).schema.names # type: ignore
    return [col for col in column_names if col != "Date"] # type: ignore

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
