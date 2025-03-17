from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias
import metrics as mt
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

RollingMetricFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
OverallMetricFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]
metrics_func: list[OverallMetricFunc] = [
    mt.get_total_returns,
    mt.overall_sharpe_ratio,
    mt.get_max_drawdown,
    mt.overall_volatility_annualized,
]


def get_metrics(returns_df: DataFrameFloat) -> SeriesFloat:
    array: ArrayFloat = returns_df.get_array()
    results: list[ArrayFloat] = [func(array) for func in metrics_func]
    names: list[str] = [
        _format_metric_name(name=func.__name__) for func in metrics_func
    ]
    results_list: list[float] = [result.item() for result in results]
    return SeriesFloat.from_float_list(data=results_list, index=names)


def _format_metric_name(name: str) -> str:
    return name.replace("_", " ").title()


@dataclass
class StatsDF:
    func: RollingMetricFunc
    ascending: bool
    title: str

    def get_data(self, data: DataFrameFloat, length: int) -> DataFrameFloat:
        array: ArrayFloat = self.func(data.get_array(), length)
        return DataFrameFloat(
            data=array,
            index=data.dates,
            columns=data.get_names(),
        ).sort_data(ascending=self.ascending)


@dataclass
class StatsSeries:
    func: OverallMetricFunc
    ascending: bool
    title: str

    def get_data(self, data: DataFrameFloat) -> SeriesFloat:
        array: ArrayFloat = self.func(data.get_array())
        return SeriesFloat(data=array, index=data.get_names()).sort_data(
            ascending=self.ascending
        )
