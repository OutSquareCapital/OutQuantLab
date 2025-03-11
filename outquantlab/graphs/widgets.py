import plotly.graph_objects as go  # type: ignore

from outquantlab.graphs.ui_constants import CustomHovers
from outquantlab.graphs.widgets_interface import (
    widget_df_interface,
    widget_serie_interface,
)
from outquantlab.graphs.widgets_setups import (
    setup_bars,
    setup_curves,
    setup_histogram,
    setup_violin,
    setup_table
)
from outquantlab.typing_conventions import (
    DataFrameFloat,
    SeriesFloat,
)


def curves(
    df: DataFrameFloat,
    title: str,
) -> go.Figure:
    return widget_df_interface(
        data=df,
        title=title,
        setup=setup_curves,
        custom_hover=CustomHovers.Y.value,
    )


def bars(series: SeriesFloat, title: str) -> go.Figure:
    return widget_serie_interface(
        data=series,
        title=title,
        setup=setup_bars,
        custom_hover=CustomHovers.Y.value,
    )

def violin(df: DataFrameFloat, title: str) -> go.Figure:
    return widget_df_interface(
        data=df,
        title=title,
        setup=setup_violin,
        custom_hover=CustomHovers.Y.value,
    )


def histogram(df: DataFrameFloat, title: str) -> go.Figure:
    return widget_df_interface(
        data=df,
        title=title,
        setup=setup_histogram,
        custom_hover=CustomHovers.X.value,
    )

def table(series: SeriesFloat, title: str) -> go.Figure:
    return widget_serie_interface(
        data=series,
        title=title,
        setup=setup_table
    )