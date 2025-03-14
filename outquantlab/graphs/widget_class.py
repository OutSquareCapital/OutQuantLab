from abc import ABC, abstractmethod

import plotly.graph_objects as go  # type: ignore

from outquantlab.graphs.widgets_interface import get_color_map
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from outquantlab.graphs.ui_constants import Colors, FigureSetup
from dataclasses import dataclass
from typing import TypeVar, Generic


T = TypeVar("T", bound=DataFrameFloat | SeriesFloat)


@dataclass
class Graph:
    custom_hover: str | None
    figure: go.Figure = go.Figure()

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
    def setup_figure_type(self, data: T, color_map: dict[str, str]) -> None:
        pass

    def get_fig(self, data: T, title: str) -> Graph:
        color_map: dict[str, str] = get_color_map(assets=data.get_names())
        self.setup_figure_type(data=data, color_map=color_map)
        self.graph.setup_style(title=title)
        return self.graph
