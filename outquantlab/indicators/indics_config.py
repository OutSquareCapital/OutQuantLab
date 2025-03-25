from outquantlab.typing_conventions import ArrayFloat
from outquantlab.indicators.params_validations import filter_valid_pairs
from abc import ABC, abstractmethod
from typing import Any

class BaseIndic(ABC):
    def __init__(
        self,
        name: str,
        active: bool,
        param_values: dict[str, list[int]],
    ) -> None:
        self.name: str = name
        self.active: bool = active
        self.params_values: dict[str, list[int]] = param_values
        self.param_combos: list[tuple[int, ...]] = []

    @abstractmethod
    def execute(*args: Any, **kwargs: Any) -> ArrayFloat: ...

    def get_valid_pairs(self) -> None:
        self.param_combos = filter_valid_pairs(params_values=self.params_values)

        if not self.param_combos:
            raise ValueError(
                f"Aucune combinaison valide trouvée pour l'indicateur {self.name}"
            )

    @property
    def params_nb(self) -> int:
        return len(self.param_combos)