from outquantlab.typing_conventions import (
    DataFrameFloat,
    SeriesFloat,
)
from typing import TypeAlias
from collections.abc import Callable
import plotly.graph_objects as go  # type: ignore
from outquantlab.graphs.ui_constants import (
    Colors,
    BASE_COLORS,
    FigureSetup,
)
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

SetupDF: TypeAlias = Callable[[DataFrameFloat, dict[str, str]], go.Figure]
SetupSeries: TypeAlias = Callable[[SeriesFloat, dict[str, str]], go.Figure]


def widget_df_interface(
    data: DataFrameFloat,
    title: str,
    setup: SetupDF,
    custom_hover: str | None = None,
) -> go.Figure:
    fig: go.Figure = setup(data, _get_color_map(assets=data.get_names()))
    _setup_figure_layout(fig=fig, figtitle=title)
    if custom_hover:
        _setup_custom_hover(fig=fig, hover_data=custom_hover)
    return fig


def widget_serie_interface(
    data: SeriesFloat,
    title: str,
    setup: SetupSeries,
    custom_hover: str | None = None,
) -> go.Figure:
    fig: go.Figure = setup(data, _get_color_map(assets=data.get_names()))
    _setup_figure_layout(fig=fig, figtitle=title)
    if custom_hover:
        _setup_custom_hover(fig=fig, hover_data=custom_hover)
    return fig


def _setup_custom_hover(fig: go.Figure, hover_data: str) -> None:
    for trace in fig.data:  # type: ignore
        trace.hovertemplate = hover_data  # type: ignore


def _setup_figure_layout(
    fig: go.Figure,
    figtitle: str,
) -> None:
    fig.update_layout(  # type: ignore
        font=FigureSetup.TEXT_FONT.value,
        title={
            "text": figtitle,
            "font": FigureSetup.TITLE_FONT.value,
        },
        autosize=True,
        margin=dict(l=30, r=30, t=40, b=30),
        paper_bgcolor=Colors.BLACK,
        plot_bgcolor=Colors.BLACK,
        legend={
            "title_font": FigureSetup.LEGEND_TITLE_FONT.value,
        },
    )

    fig.update_yaxes(  # type: ignore
        showgrid=False, automargin=True
    )

    fig.update_xaxes(  # type: ignore
        showgrid=False, automargin=True
    )


def _get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = _map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))


def _map_colors_to_columns(n_colors: int) -> list[str]:
    if n_colors == 1:
        return [mcolors.to_hex(Colors.PLOT_UNIQUE)]
    colormap: LinearSegmentedColormap = _generate_colormap(n_colors=n_colors)
    return [mcolors.to_hex(colormap(i / (n_colors - 1))) for i in range(n_colors)]


def _generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    cmap_name = "custom_colormap"

    if n_colors <= len(BASE_COLORS):
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=BASE_COLORS[:n_colors], N=n_colors
        )
    else:
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=BASE_COLORS, N=n_colors
        )
