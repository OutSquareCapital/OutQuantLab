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
        return f"{self.name} \n {self.active} \n {self.params}"

    @abstractmethod
    def execute(*args: Any, **kwargs: Any) -> arrays.ArrayFloat: ...

    def process_params_parallel(
        self,
        data_arrays: DataArrays,
        global_executor: ThreadPoolExecutor,
    ) -> list[arrays.ArrayFloat]:
        def process_single_param(param_tuple: tuple[int, ...]) -> arrays.ArrayFloat:
            signal: arrays.ArrayFloat = rolling_scalar_normalisation(
                raw_signal=self.execute(data_arrays, *param_tuple)
            )
            # signal: arrays.ArrayFloat = long_bias_normalization(signal_array=signal)
            return signal * data_arrays.pct_returns  # temporary

        return list(global_executor.map(process_single_param, self.params.combos))
