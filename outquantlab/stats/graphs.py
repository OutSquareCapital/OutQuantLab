from abc import ABC, abstractmethod

import plotly.graph_objects as go  # type: ignore

from outquantlab.stats.design import (
    Colors,
    CustomHovers,
    FigureSetup,
    get_color_map,
    get_heatmap_colorscale,
    get_marker_config,
)
import tradeframe as tf


class Graph[
    D:tf.FrameVertical
    | dict[str, float]
](ABC):
    def __init__(self, formatted_data: D, title: str) -> None:
        self.figure = go.Figure()
        self.setup_figure(formatted_data=formatted_data)
        self._setup_general_design(title=title)
        self._setup_axes()
        self.figure.show()  # type: ignore

    @abstractmethod
    def setup_figure(self, formatted_data: D) -> None:
        raise NotImplementedError

    def _setup_general_design(self, title: str) -> None:
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


class Curves(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.values:
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    y=column,
                    mode="lines",
                    name=column.name,
                    line=dict(width=2, color=color_map[column.name]),
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class LogCurves(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.values:
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    y=column,
                    mode="lines",
                    name=column.name,
                    line=dict(width=2, color=color_map[column.name]),
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )
        self.figure.update_yaxes(  # type: ignore
            type="log"
        )


class Violins(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.values:
            self.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=column,
                    name=column.name,
                    box_visible=True,
                    points=False,
                    marker=get_marker_config(color=color_map[column.name]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class Boxes(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.values:
            self.figure.add_trace(  # type: ignore
                trace=go.Box(
                    y=column,
                    name=column.name,
                    marker=get_marker_config(color=color_map[column.name]),
                    boxpoints=False,
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class Histograms(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.values:
            self.figure.add_trace(  # type: ignore
                trace=go.Histogram(
                    x=column,
                    name=column.name,
                    marker=get_marker_config(color=color_map[column.name]),
                    hovertemplate=CustomHovers.HORIZONTAL_DATA.value,
                )
            )
        self.figure.update_layout(  # type: ignore
            barmode="overlay"
        )


class Bars(Graph[dict[str, float]]):
    def setup_figure(self, formatted_data: dict[str, float]) -> None:

        color_map: dict[str, str] = get_color_map(assets=list(formatted_data.keys()))
        for label, value in formatted_data.items():
            self.figure.add_trace(  # type: ignore
                trace=go.Bar(
                    x=[label],
                    y=[value],
                    name=label,
                    marker=get_marker_config(color=color_map[label]),
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )

        self.figure.update_layout(  # type: ignore
            xaxis=dict(showticklabels=False)
        )


class HeatMap(Graph[tf.FrameVertical]):
    def setup_figure(self, formatted_data: tf.FrameVertical) -> None:
        color_scale: list[list[float | str]] = get_heatmap_colorscale()
        self.figure.add_trace(  # type: ignore
            trace=go.Heatmap(
                z=formatted_data.get_array(),
                x=formatted_data.get_names(),
                y=formatted_data.get_names(),
                showscale=False,
                colorscale=color_scale,
                hovertemplate=CustomHovers.HEATMAP.value,
            )
        )
        self.figure.update_layout(  # type: ignore
            yaxis=dict(showgrid=False, autorange="reversed")
        )
        self.figure.update_yaxes(showticklabels=False, scaleanchor="x")  # type: ignore
        self.figure.update_xaxes(showticklabels=False)  # type: ignore
