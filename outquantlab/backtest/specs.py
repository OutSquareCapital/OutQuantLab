from dataclasses import dataclass
from os import cpu_count

from outquantlab.indicators import BaseIndic
from outquantlab.structures import arrays


@dataclass(slots=True, frozen=True)
class Dimensions:
    assets: int
    days: int
    indics: int
    params: int

    @property
    def total(self) -> int:
        return self.assets * self.params

    def get_main_array(self) -> arrays.Float2D:
        return arrays.create_empty(length=self.days, width=self.total)


class BacktestSpecs:
    def __init__(self, pct_returns: arrays.Float2D, indics: list[BaseIndic]) -> None:
        self.thread_nb: int = cpu_count() or 8
        self.current_index: int = 0
        self.dims = Dimensions(
            assets=pct_returns.shape[1],
            days=pct_returns.shape[0],
            indics=len(indics),
            params=sum([indic.params.quantity for indic in indics]),
        )

    def fill_main_array(
        self, main_array: arrays.Float2D, results_list: list[arrays.Float2D]
    ) -> None:
        for i in range(len(results_list)):
            end_index: int = self.current_index + self.dims.assets
            main_array[:, self.current_index : end_index] = results_list[i]
            self.current_index = end_index


class BacktestError(Exception):
    def __init__(
        self,
        indic: BaseIndic,
        specs: BacktestSpecs,
        e: Exception,
    ) -> None:
        super().__init__(
            f"Error during backtest.\n Issue: {e} \n Specs:\n {specs}\n Indicator:\n {indic}"
        )
