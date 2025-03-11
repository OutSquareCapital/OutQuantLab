from collections.abc import Callable
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat, ArrayFloat
from typing import TypeAlias

RollingMetricFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
OverallMetricFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]

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
