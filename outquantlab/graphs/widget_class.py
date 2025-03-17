from abc import ABC, abstractmethod

import plotly.graph_objects as go  # type: ignore

from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from outquantlab.graphs.ui_constants import Colors, FigureSetup, BASE_COLORS
from typing import TypeVar, Generic
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors

T = TypeVar("T", bound=DataFrameFloat | SeriesFloat)


class Graph:
    def __init__(self, custom_hover: str | None) -> None:
        self.custom_hover: str | None = custom_hover
        self.figure: go.Figure = go.Figure()

    def show(self) -> None:
        self.figure.show()  # type: ignore

    def setup_style(self, title: str) -> None:
        self._setup_design(title=title)
        self._setup_axes()
        if self.custom_hover:
            self._setup_custom_hover()

    def _setup_design(
        self,
        title: str,
    ) -> None:
        self.figure.update_layout(  # type: ignore
            font=FigureSetup.TEXT_FONT.value,
            title={
                "text": title,
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

    def _setup_axes(self) -> None:
        self.figure.update_yaxes(  # type: ignore
            showgrid=False, automargin=True
        )

        self.figure.update_xaxes(  # type: ignore
            showgrid=False, automargin=True
        )

    def _setup_custom_hover(self) -> None:
        for trace in self.figure.data:  # type: ignore
            trace.hovertemplate = self.custom_hover  # type: ignore


class BaseWidget(ABC, Generic[T]):
    def __init__(self, custom_hover: str | None) -> None:
        self.graph = Graph(custom_hover=custom_hover)

    @abstractmethod
    def _setup_figure_type(self, data: T, color_map: dict[str, str]) -> None:
        pass

    def get_fig(self, data: T, title: str) -> Graph:
        color_map: dict[str, str] = _get_color_map(assets=data.get_names())
        self._setup_figure_type(data=data, color_map=color_map)
        self.graph.setup_style(title=title)
        return self.graph

    def _get_marker_config(
        self, color: str
    ) -> dict[str, str | dict[str, Colors | int]]:
        return dict(color=color, line=dict(color=Colors.WHITE, width=1))


def _get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))


def map_colors_to_columns(n_colors: int) -> list[str]:
    if n_colors == 1:
        return [mcolors.to_hex(Colors.PLOT_UNIQUE.value)]
    cmap: LinearSegmentedColormap = _generate_colormap(n_colors=n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]


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
