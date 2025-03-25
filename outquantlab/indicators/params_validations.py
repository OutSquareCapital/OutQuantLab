from collections.abc import Callable
from itertools import product
from dataclasses import dataclass, field

ParamsValidator = Callable[[dict[str, int]], bool]
ValidationProcess = tuple[ParamsValidator, ParamsValidator]

@dataclass(slots=True)
class IndicParams:
    values: dict[str, list[int]]
    combos: list[tuple[int, ...]] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return f"values: \n {self.values} \n combos: \n {self.combos}"
    @property
    def quantity(self) -> int:
        return len(self.combos)

    def get_valid_pairs(self) -> None:
        parameter_names = list(self.values.keys())
        parameter_values_combinations = product(*self.values.values())

        for combination in parameter_values_combinations:
            combination_dict = dict(zip(parameter_names, combination))
            if _validate_combination(parameters_dict=combination_dict):
                self.combos.append(combination)

        if not self.combos:
            raise ValueError(
                f"Aucune combinaison valide trouvée pour l'indicateur {self}"
            )

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


_VALIDATION_RULES: list[ValidationProcess] = [
    (_check_trend, _validate_trend),
    (_check_skew, _validate_skew),
]


def _validate_combination(parameters_dict: dict[str, int]) -> bool:
    for check, validate in _VALIDATION_RULES:
        if check(parameters_dict):
            if not validate(parameters_dict):
                return False
    return True
