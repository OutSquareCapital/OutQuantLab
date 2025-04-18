from abc import ABC, abstractmethod
from typing import Protocol, TypeAlias, Any, NamedTuple

import numquant as nq
from itertools import product
from dataclasses import dataclass

class ParamResult(NamedTuple):
    indic: str
    param: str
    data: nq.Float2D

class AssetsData(Protocol):
    prices: nq.Float2D
    log_returns: nq.Float2D
    pct_returns: nq.Float2D
    adjusted_returns: nq.Float2D


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
    def execute(self, data: AssetsData, params: T) -> nq.Float2D:
        raise NotImplementedError

    @abstractmethod
    def _get_combo(self, combination: tuple[int, ...]) -> T:
        raise NotImplementedError

    def process_single_param(self, data_arrays: AssetsData, param_tuple: T) -> ParamResult:
        data = self.normalize_signal(
                signal=self.execute(data=data_arrays, params=param_tuple),
                long_only=False,
            ) * data_arrays.adjusted_returns
        return ParamResult(
            indic=self.name,
            param=param_tuple.get_names(),
            data=data
        )
    def normalize_signal(
        self, signal: nq.Float2D, long_only: bool
    ) -> nq.Float2D:
        if long_only:
            return nq.metrics.roll.long_bias_normalization(
                signal_array=nq.metrics.roll.rolling_scalar_normalisation(raw_signal=signal)
            )
        return nq.metrics.roll.rolling_scalar_normalisation(raw_signal=signal)

    def __repr__(self) -> str:
        return f"name: {self.name} \n statut: {self.active} \n params:\n {self.params_values}"


GenericIndic: TypeAlias = BaseIndic[Any]
