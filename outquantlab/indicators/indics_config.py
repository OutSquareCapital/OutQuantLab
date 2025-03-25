from outquantlab.typing_conventions import ArrayFloat
from outquantlab.indicators.data_arrays import DataArrays
from outquantlab.indicators.params_validations import IndicParams
from outquantlab.metrics import rolling_scalar_normalisation
from abc import ABC, abstractmethod
from typing import Any
from concurrent.futures import ThreadPoolExecutor

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
    def execute(*args: Any, **kwargs: Any) -> ArrayFloat: ...

    def process_params_parallel(
        self,
        data_arrays: DataArrays,
        global_executor: ThreadPoolExecutor,
    ) -> list[ArrayFloat]:
        def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
            return (
                rolling_scalar_normalisation(
                    raw_signal=self.execute(data_arrays, *param_tuple)
                )
                * data_arrays.adjusted_returns
            )

        return list(global_executor.map(process_single_param, self.params.combos))
