from collections.abc import Callable
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat, ArrayFloat
from typing import TypeAlias
import outquantlab.metrics as mt
from enum import Enum

RollingMetricFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
OverallMetricFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]


class MetricFuncs(Enum):
    total_returns: OverallMetricFunc = mt.calculate_total_returns
    sharpe_ratio: OverallMetricFunc = mt.overall_sharpe_ratio
    max_drawdown: OverallMetricFunc = mt.calculate_max_drawdown
    volatility: OverallMetricFunc = mt.overall_volatility_annualized


def get_df_stats_interface(
    returns_df: DataFrameFloat,
    metric_func: RollingMetricFunc,
    ascending: bool,
    length: int,
) -> DataFrameFloat:
    return DataFrameFloat(
        data=metric_func(returns_df.get_array(), length),
        index=returns_df.dates,
        columns=returns_df.get_names(),
    ).sort_data(ascending=ascending)


def get_series_stats_interface(
    returns_df: DataFrameFloat,
    metric_func: OverallMetricFunc,
    ascending: bool,
) -> SeriesFloat:
    return SeriesFloat(
        data=metric_func(returns_df.get_array()),
        index=returns_df.get_names(),
    ).sort_data(ascending=ascending)
