from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from outquantlab.indicators.data_arrays import DataArrays
from outquantlab.indicators.params_validations import IndicParams
from outquantlab.metrics import (
    rolling_scalar_normalisation,
)  # , long_bias_normalization
from outquantlab.structures import arrays


class BaseIndic(ABC):
    def __init__(
        self,
        name: str,
        active: bool,
        param_values: dict[str, list[int]],
    ) -> None:
        self.name: str = name
        self.active: bool = active
        self.params: IndicParams = IndicParams(values=param_values)

    def __repr__(self) -> str:
        return f"name: {self.name} \n statut: {self.active} \n params: {self.params}"

    @abstractmethod
    def execute(*args: Any, **kwargs: Any) -> arrays.Float2D: ...

    def process_params_parallel(
        self,
        data_arrays: DataArrays,
        global_executor: ThreadPoolExecutor,
    ) -> list[arrays.Float2D]:
        def process_single_param(param_tuple: tuple[int, ...]) -> arrays.Float2D:
            signal: arrays.Float2D = rolling_scalar_normalisation(
                raw_signal=self.execute(data_arrays, *param_tuple)
            )
            # signal: arrays.Float2D = long_bias_normalization(signal_array=signal)
            return signal * data_arrays.pct_returns  # temporary

        return list(global_executor.map(process_single_param, self.params.combos))
