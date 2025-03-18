from collections.abc import Callable
from typing import TypeAlias
import outquantlab.metrics as mt
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

RollingMetricFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
OverallMetricFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]


def _format_name(name: str) -> str:
    return name.replace("get", "").replace("_", " ").title()


class StatsOverall:
    def __init__(self, data: DataFrameFloat) -> None:
        self.metrics_func: list[OverallMetricFunc] = [
            mt.get_total_returns,
            mt.overall_sharpe_ratio,
            mt.get_max_drawdown,
            mt.overall_volatility_annualized,
        ]
        self.data: SeriesFloat = self.get_data(returns_df=data)
        self.title: str = "Overall Stats"

    def get_data(self, returns_df: DataFrameFloat) -> SeriesFloat:
        array: ArrayFloat = returns_df.get_array()
        results: list[ArrayFloat] = [func(array) for func in self.metrics_func]
        names: list[str] = [
            _format_name(name=func.__name__) for func in self.metrics_func
        ]
        results_list: list[float] = [result.item() for result in results]
        return SeriesFloat.from_float_list(data=results_list, index=names)


class StatsDF:
    def __init__(
        self,
        data: DataFrameFloat,
        func: RollingMetricFunc,
        ascending: bool,
        length: int,
    ) -> None:
        self.func: RollingMetricFunc = func
        self.data: DataFrameFloat = self.get_data(
            data=data, ascending=ascending, length=length
        )
        self.title: str = _format_name(name=func.__name__)

    def get_data(
        self, data: DataFrameFloat, ascending: bool, length: int
    ) -> DataFrameFloat:
        array: ArrayFloat = self.func(data.get_array(), length)
        return DataFrameFloat(
            data=array,
            index=data.dates,
            columns=data.get_names(),
        ).sort_data(ascending=ascending)


class StatsSeries:
    def __init__(
        self,
        data: DataFrameFloat,
        func: OverallMetricFunc,
        ascending: bool,
    ) -> None:
        self.func: OverallMetricFunc = func
        self.data: SeriesFloat = self.get_data(data=data, ascending=ascending)
        self.title: str = _format_name(name=func.__name__)

    def get_data(self, data: DataFrameFloat, ascending: bool) -> SeriesFloat:
        array: ArrayFloat = self.func(data.get_array())
        return SeriesFloat(data=array, index=self.data.get_names()).sort_data(
            ascending=ascending
        )
