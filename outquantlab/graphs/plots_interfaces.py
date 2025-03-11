from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from typing import TypeAlias
from collections.abc import Callable
import plotly.graph_objects as go  # type: ignore

StatSerieInterface: TypeAlias = Callable[[DataFrameFloat], SeriesFloat]
StatDataFrameInterface: TypeAlias = Callable[[DataFrameFloat, int], DataFrameFloat]
SeriesWidget: TypeAlias = Callable[[SeriesFloat, str], go.Figure]
DataframeWidget: TypeAlias = Callable[[DataFrameFloat, str], go.Figure]


def _format_plot_name(name: str) -> str:
    return name.replace("plot", "").replace("_", " ").title()


def get_df_plot_interface(
    returns_df: DataFrameFloat,
    widget_func: DataframeWidget,
    stats_func: StatDataFrameInterface,
    length: int,
) -> go.Figure:
    return widget_func(
        stats_func(returns_df, length),
        _format_plot_name(name=stats_func.__name__),
    )


def get_serie_plot_interface(
    returns_df: DataFrameFloat,
    widget_func: SeriesWidget,
    stats_func: StatSerieInterface,
) -> go.Figure:
    return widget_func(
        stats_func(returns_df),
        _format_plot_name(name=stats_func.__name__),
    )
