from os import cpu_count

from numpy import empty
from pandas import DatetimeIndex, MultiIndex

from outquantlab.typing_conventions import ArrayFloat, Float32
from outquantlab.indicators import ReturnsData, BaseIndic


class BacktestSpecs:
    def __init__(
        self,
        returns_data: ReturnsData,
        indics_params: list[BaseIndic],
        multi_index: MultiIndex,
    ) -> None:
        self.observations_nb: int = returns_data.prices_array.shape[0]
        self.assets_count: int = returns_data.prices_array.shape[1]
        self.strategies_nb: int = sum(
            [len(indic.param_combos) for indic in indics_params]
        )
        self.threads_nb: int = cpu_count() or 8
        self.dates: DatetimeIndex = returns_data.global_returns.dates
        self.multi_index: MultiIndex = multi_index
        self.total_returns_streams: int = self.assets_count * self.strategies_nb

    def get_signals_array(self) -> ArrayFloat:
        return empty(
            shape=(self.observations_nb, self.total_returns_streams), dtype=Float32
        )
