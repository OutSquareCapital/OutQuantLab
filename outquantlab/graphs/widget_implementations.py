import plotly.graph_objects as go  # type: ignore
from outquantlab.graphs.ui_constants import Colors, CustomHovers
from outquantlab.graphs.widget_class import BaseWidget
import outquantlab.metrics as mt
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat


class Curves(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(
        self, data: DataFrameFloat, color_map: dict[str, str]
    ) -> None:
        for column in data.get_names():
            self.graph.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=data.dates,
                    y=data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=color_map[column]),
                )
            )


class Violins(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(
        self, data: DataFrameFloat, color_map: dict[str, str]
    ) -> None:
        for column in data.columns:
            self.graph.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=data[column],
                    name=column,
                    box_visible=True,
                    points=False,
                    marker=self._get_marker_config(color=color_map[column]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                )
            )

        min_by_column: ArrayFloat = mt.get_overall_min(array=data.get_array())
        y_min: ArrayFloat = mt.get_overall_min(array=min_by_column)

        max_by_column: ArrayFloat = mt.get_overall_max(array=data.get_array())
        y_max: ArrayFloat = mt.get_overall_max(array=max_by_column)

        self.graph.figure.update_layout(  # type: ignore
            yaxis=dict(range=[y_min, y_max], showgrid=False),
            xaxis=dict(
                showticklabels=False,
            ),
        )


class Histogram(BaseWidget[DataFrameFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.X.value)

    def _setup_figure_type(
        self, data: DataFrameFloat, color_map: dict[str, str]
    ) -> None:
        for column in data.columns:
            self.graph.figure.add_trace(  # type: ignore
                trace=go.Histogram(
                    x=data[column],
                    name=column,
                    marker=self._get_marker_config(color=color_map[column]),
                )
            )
        self.graph.figure.update_layout(  # type: ignore
            barmode="overlay"
        )


class Bars(BaseWidget[SeriesFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=CustomHovers.Y.value)

    def _setup_figure_type(self, data: SeriesFloat, color_map: dict[str, str]) -> None:
        for label, value in zip(data.get_names(), data.get_array()):
            self.graph.figure.add_trace(  # type: ignore
                trace=go.Bar(
                    x=[label],
                    y=[value],
                    name=label,
                    marker=self._get_marker_config(color=color_map[label]),
                )
            )

        self.graph.figure.update_layout(  # type: ignore
            xaxis=dict(showticklabels=False)
        )


class Table(BaseWidget[SeriesFloat]):
    def __init__(self) -> None:
        super().__init__(custom_hover=None)

    def _setup_figure_type(self, data: SeriesFloat, color_map: dict[str, str]) -> None:
        self.graph.figure.add_trace(  # type: ignore
            trace=go.Table(
                header=dict(values=["Metric", "Value"], fill_color=Colors.BLACK),
                cells=dict(
                    values=[data.get_names(), data.get_array()],
                    fill_color=[color_map[name] for name in data.get_names()],
                ),
            )
        )
