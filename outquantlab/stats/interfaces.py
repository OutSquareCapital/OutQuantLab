from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat, StatFunc
from typing import Any

def get_df_stats_interface(
    returns_df: DataFrameFloat,
    stats_func: StatFunc,
    ascending: bool,
    **kwargs: Any,
) -> DataFrameFloat:
    return DataFrameFloat(
        data=stats_func(returns_df.get_array(), **kwargs),
        index=returns_df.dates,
        columns=returns_df.get_names(),
    ).sort_data(ascending=ascending)


def get_series_stats_interface(
    returns_df: DataFrameFloat,
    stats_func: StatFunc,
    ascending: bool,
    **kwargs: Any,
) -> SeriesFloat:
    return SeriesFloat(
        data=stats_func(returns_df.get_array(), **kwargs),
        index=returns_df.get_names(),
    ).sort_data(ascending=ascending)
