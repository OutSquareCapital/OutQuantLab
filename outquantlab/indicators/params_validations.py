from collections.abc import Callable
from itertools import product

ValidationPredicate = Callable[[dict[str, int]], bool]
ValidationRule = tuple[ValidationPredicate, ValidationPredicate]

# TODO: integrer name de la class indic afin de pouvoir directement lier le check a l'indic

def _check_trend(params: dict[str, int]) -> bool:
    return bool(next((k for k in params if "st" in k), None)) and bool(
        next((k for k in params if "lt" in k), None)
    )


def _validate_trend(params: dict[str, int]) -> bool:
    st_param: str = next(k for k in params if "st" in k)
    lt_param: str = next(k for k in params if "lt" in k)
    return params[st_param] * 4 <= params[lt_param]


def _check_skew(params: dict[str, int]) -> bool:
    return "len_smooth" in params and "len_skew" in params and params["len_smooth"] > 1


def _validate_skew(params: dict[str, int]) -> bool:
    return params["len_smooth"] * 8 <= params["len_skew"]


_VALIDATION_RULES: list[ValidationRule] = [
    (_check_trend, _validate_trend),
    (_check_skew, _validate_skew),
]


def _validate_combination(parameters_dict: dict[str, int]) -> bool:
    for check, validate in _VALIDATION_RULES:
        if check(parameters_dict):
            if not validate(parameters_dict):
                return False
    return True


def filter_valid_pairs(params_values: dict[str, list[int]]) -> list[tuple[int, ...]]:
    parameter_names = list(params_values.keys())
    parameter_values_combinations = product(*params_values.values())

    valid_combinations: list[tuple[int, ...]] = []

    for combination in parameter_values_combinations:
        combination_dict = dict(zip(parameter_names, combination))
        if _validate_combination(parameters_dict=combination_dict):
            valid_combinations.append(combination)

    return valid_combinations
