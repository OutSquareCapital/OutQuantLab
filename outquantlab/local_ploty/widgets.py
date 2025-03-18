from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import plotly.graph_objects as go  # type: ignore

import outquantlab.metrics as mt
from outquantlab.local_ploty.graph_class import Graph
from outquantlab.local_ploty.ui_constants import Colors, CustomHovers
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

T = TypeVar("T", bound=DataFrameFloat | SeriesFloat)


class BaseWidget(ABC, Generic[T]):
    def __init__(self, custom_hover: str | None) -> None:
        self.custom_hover: str | None = custom_hover

    @abstractmethod
    def _setup_figure_type(self, graph: Graph, data: T) -> None:
        pass

    def get_fig(self, data: T, title: str) -> Graph:
        graph = Graph(
            custom_hover=self.custom_hover,
            title=title,
            assets=data.get_names(),
        )
        self._setup_figure_type(graph=graph, data=data)
        graph.setup_style()
        return graph

    def _get_marker_config(
        self, color: str
    ) -> dict[str, str | dict[str, Colors | int]]:
        return dict(color=color, line=dict(color=Colors.WHITE, width=1))


class Curves(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(self, graph: Graph, data: DataFrameFloat) -> None:
        for column in data.get_names():
            graph.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=data.dates,
                    y=data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=graph.color_map[column]),
                )
            )


class Violins(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(self, graph: Graph, data: DataFrameFloat) -> None:
        for column in data.columns:
            graph.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=data[column],
                    name=column,
                    box_visible=True,
                    points=False,
                    marker=self._get_marker_config(color=graph.color_map[column]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                )
            )

        min_by_column: ArrayFloat = mt.get_overall_min(array=data.get_array())
        y_min: ArrayFloat = mt.get_overall_min(array=min_by_column)

        max_by_column: ArrayFloat = mt.get_overall_max(array=data.get_array())
        y_max: ArrayFloat = mt.get_overall_max(array=max_by_column)

        graph.figure.update_layout(  # type: ignore
            yaxis=dict(range=[y_min, y_max], showgrid=False),
            xaxis=dict(
                showticklabels=False,
            ),
        )


class Histogram(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.X.value)

    def _setup_figure_type(self, graph: Graph, data: DataFrameFloat) -> None:
        for column in data.columns:
            graph.figure.add_trace(  # type: ignore
                trace=go.Histogram(
                    x=data[column],
                    name=column,
                    marker=self._get_marker_config(color=graph.color_map[column]),
                )
            )
        graph.figure.update_layout(  # type: ignore
            barmode="overlay"
        )


class Bars(BaseWidget[SeriesFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(self, graph: Graph, data: SeriesFloat) -> None:
        for label, value in zip(
            data.get_names(),
            data.get_array(),
        ):
            graph.figure.add_trace(  # type: ignore
                trace=go.Bar(
                    x=[label],
                    y=[value],
                    name=label,
                    marker=self._get_marker_config(color=graph.color_map[label]),
                )
            )

        graph.figure.update_layout(  # type: ignore
            xaxis=dict(showticklabels=False)
        )


class Table(BaseWidget[SeriesFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=None)

    def _setup_figure_type(self, graph: Graph, data: SeriesFloat) -> None:
        graph.figure.add_trace(  # type: ignore
            trace=go.Table(
                header=dict(values=["Metric", "Value"], fill_color=Colors.BLACK),
                cells=dict(
                    values=[
                        data.get_names(),
                        data.get_array(),
                    ],
                    fill_color=[
                        Colors.PLOT_UNIQUE
                    ],
                ),
            )
        )
