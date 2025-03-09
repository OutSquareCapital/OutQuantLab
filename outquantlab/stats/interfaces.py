from outquantlab.typing_conventions import (
    DataFrameFloat,
    SeriesFloat,
    OverallStatFunc,
    RollingStatFunc,
)


def get_df_stats_interface(
    returns_df: DataFrameFloat,
    stats_func: RollingStatFunc,
    ascending: bool,
    length: int,
) -> DataFrameFloat:
    return DataFrameFloat(
        data=stats_func(returns_df.get_array(), length),
        index=returns_df.dates,
        columns=returns_df.get_names(),
    ).sort_data(ascending=ascending)


def get_series_stats_interface(
    returns_df: DataFrameFloat,
    stats_func: OverallStatFunc,
    ascending: bool,
) -> SeriesFloat:
    return SeriesFloat(
        data=stats_func(returns_df.get_array()),
        index=returns_df.get_names(),
    ).sort_data(ascending=ascending)
