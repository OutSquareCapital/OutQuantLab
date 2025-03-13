from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeAlias

import plotly.graph_objects as go  # type: ignore

from outquantlab.graphs.widgets_interface import get_color_map
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from outquantlab.graphs.ui_constants import Colors, FigureSetup

StatSerieInterface: TypeAlias = Callable[[DataFrameFloat], SeriesFloat]
StatDataFrameInterface: TypeAlias = Callable[[DataFrameFloat, int], DataFrameFloat]


class WidgetDataFrame(ABC):
    def __init__(self, custom_hover: str|None) -> None:
        self.custom_hover: str | None = custom_hover
        self.figure: go.Figure = go.Figure()

    def get_fig(
        self, data: DataFrameFloat, length: int, stats_func: StatDataFrameInterface
    ) -> go.Figure:
        formatted_data: DataFrameFloat = stats_func(data, length)
        title: str = _format_plot_name(name=stats_func.__name__)
        self.format_fig(data=formatted_data, title=title)
        return self.figure

    def format_fig(
        self,
        data: DataFrameFloat,
        title: str,
    ) -> None:
        color_map: dict[str, str] = get_color_map(assets=data.get_names())
        self.setup_figure_type(data=data, color_map=color_map)
        self.setup_figure_layout(title=title)
        if self.custom_hover is not None:
            self.setup_custom_hover()

    @abstractmethod
    def setup_figure_type(self, data: DataFrameFloat, color_map: dict[str, str]) -> None:
        pass

    def setup_figure_layout(
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

        self.figure.update_yaxes(  # type: ignore
            showgrid=False, automargin=True
        )

        self.figure.update_xaxes(  # type: ignore
            showgrid=False, automargin=True
        )

    def setup_custom_hover(self) -> None:
        for trace in self.figure.data:  # type: ignore
            trace.hovertemplate = self.custom_hover  # type: ignore


def _format_plot_name(name: str) -> str:
    return name.replace("get", "").replace("_", " ").title()
