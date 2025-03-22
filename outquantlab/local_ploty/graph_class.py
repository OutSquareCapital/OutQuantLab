import plotly.graph_objects as go  # type: ignore

from outquantlab.local_ploty.ui_constants import Colors, FigureSetup
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat

T = TypeVar("T", bound=DataFrameFloat | SeriesFloat)

class Graph(ABC, Generic[T]):
    def __init__(self, formatted_data: T, title: str) -> None:
        self.figure: go.Figure = go.Figure()
        self._setup_figure_type(formatted_data=formatted_data)
        self._setup_general_design(title=title)
        self._setup_axes()
        self.figure.show()  # type: ignore

    @abstractmethod
    def _setup_figure_type(self, formatted_data: T) -> None:
        raise NotImplementedError

    def _setup_general_design(
        self,
        title: str
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