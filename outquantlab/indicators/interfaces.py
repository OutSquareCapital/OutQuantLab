from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Protocol, TypeAlias, Any

from outquantlab.metrics import rolling_scalar_normalisation, long_bias_normalization
from outquantlab.structures import arrays
from itertools import product
from dataclasses import dataclass


class AssetsData(Protocol):
    prices: arrays.Float2D
    log_returns: arrays.Float2D
    pct_returns: arrays.Float2D
    adjusted_returns: arrays.Float2D


@dataclass(slots=True)
class BaseParams(ABC):
    values: tuple[int, ...]

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError

    def get_names(self) -> str:
        return "_".join([str(value) for value in self.values])


class BaseIndic[T: BaseParams](ABC):
    def __init__(
        self,
        name: str,
        active: bool,
        param_values: dict[str, list[int]],
    ) -> None:
        self.name: str = name
        self.active: bool = active
        self.params_values: dict[str, list[int]] = param_values
        self.combos: list[T] = []

    @property
    def quantity(self) -> int:
        return len(self.combos)

    def get_combo_names(self) -> list[str]:
        return [combo.get_names() for combo in self.combos]

    def get_all_combinations(self) -> list[tuple[int, ...]]:
        return list(product(*self.params_values.values()))

    def get_valid_pairs(self) -> None:
        all_combinations: list[tuple[int, ...]] = self.get_all_combinations()
        for combination in all_combinations:
            combo: T = self._get_combo(combination)
            if combo.validate():
                self.combos.append(combo)
        if not self.combos:
            raise ValueError(
                f"Aucune combinaison valide trouvée pour l'indicateur {self}"
            )

    @abstractmethod
    def execute(self, data: AssetsData, params: T) -> arrays.Float2D:
        raise NotImplementedError

    @abstractmethod
    def _get_combo(self, combination: tuple[int, ...]) -> T:
        raise NotImplementedError

    def process_params_parallel(
        self,
        data_arrays: AssetsData,
        global_executor: ThreadPoolExecutor,
    ) -> list[arrays.Float2D]:
        def process_single_param(param_tuple: T) -> arrays.Float2D:
            return (
                self.normalize_signal(
                    signal=self.execute(data=data_arrays, params=param_tuple),
                    long_only=False,
                )
                * data_arrays.adjusted_returns
            )

        return list(global_executor.map(process_single_param, self.combos))

    def normalize_signal(
        self, signal: arrays.Float2D, long_only: bool
    ) -> arrays.Float2D:
        if long_only:
            return long_bias_normalization(
                signal_array=rolling_scalar_normalisation(raw_signal=signal)
            )
        return rolling_scalar_normalisation(raw_signal=signal)

    def __repr__(self) -> str:
        return f"name: {self.name} \n statut: {self.active} \n params:\n {self.params_values}"


GenericIndic: TypeAlias = BaseIndic[Any]
