from outquantlab.typing_conventions import ArrayFloat
from abc import ABC, abstractmethod
from typing import Any
from itertools import product
from outquantlab.indicators.indics_data import ReturnsData


class BaseIndic(ABC):
    def __init__(
        self,
        name: str,
        active: bool,
        param_values: dict[str, list[int]],
        returns_data: ReturnsData,
    ) -> None:
        self.name: str = name
        self.active: bool = active
        self.params_values: dict[str, list[int]] = param_values
        self.param_combos: list[tuple[int, ...]] = []
        self.returns_data: ReturnsData = returns_data

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> ArrayFloat: ...

    def filter_valid_pairs(self) -> list[tuple[int, ...]]:
        parameter_names = list(self.params_values.keys())
        parameter_values_combinations = product(*self.params_values.values())
        valid_pairs: list[tuple[int, ...]] = []

        for combination in parameter_values_combinations:
            combination_dict = dict(zip(parameter_names, combination))
            if is_valid_combination(parameters_dict=combination_dict):
                valid_pairs.append(combination)

        return valid_pairs


def is_valid_combination(parameters_dict: dict[str, int]) -> bool:
    short_term_param = next((k for k in parameters_dict if "st" in k), None)
    long_term_param = next((k for k in parameters_dict if "lt" in k), None)

    if short_term_param and long_term_param:
        if parameters_dict[short_term_param] * 4 > parameters_dict[long_term_param]:
            return False

    if "len_smooth" in parameters_dict and "len_skew" in parameters_dict:
        if (
            parameters_dict["len_smooth"] > 1
            and parameters_dict["len_smooth"] * 8 > parameters_dict["len_skew"]
        ):
            return False

    return True
