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
from outquantlab.structures import frames


class Graph[D:frames.DatedFloat | frames.DefaultFloat | frames.SeriesFloat](ABC):
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


class Curves(Graph[frames.DatedFloat]):
    def setup_figure(self, formatted_data:frames.DatedFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=formatted_data.get_index(),
                    y=formatted_data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=color_map[column]),
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class LogCurves(Graph[frames.DatedFloat]):
    def setup_figure(self, formatted_data:frames.DatedFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=formatted_data.get_index(),
                    y=formatted_data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=color_map[column]),
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )
        self.figure.update_yaxes(  # type: ignore
            type="log"
        )


class Violins(Graph[frames.DefaultFloat]):
    def setup_figure(self, formatted_data: frames.DefaultFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=formatted_data[column],
                    name=column,
                    box_visible=True,
                    points=False,
                    marker=get_marker_config(color=color_map[column]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class Boxes(Graph[frames.DefaultFloat]):
    def setup_figure(self, formatted_data: frames.DefaultFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Box(
                    y=formatted_data[column],
                    name=column,
                    marker=get_marker_config(color=color_map[column]),
                    boxpoints=False,
                    hovertemplate=CustomHovers.VERTICAL_DATA.value,
                )
            )


class Histograms(Graph[frames.DefaultFloat]):
    def setup_figure(self, formatted_data:frames.DefaultFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Histogram(
                    x=formatted_data[column],
                    name=column,
                    marker=get_marker_config(color=color_map[column]),
                    hovertemplate=CustomHovers.HORIZONTAL_DATA.value,
                )
            )
        self.figure.update_layout(  # type: ignore
            barmode="overlay"
        )


class Bars(Graph[frames.SeriesFloat]):
    def setup_figure(self, formatted_data: frames.SeriesFloat) -> None:
        color_map: dict[str, str] = get_color_map(assets=formatted_data.get_names())
        for label, value in zip(
            formatted_data.get_names(),
            formatted_data.get_array(),
        ):
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


class HeatMap(Graph[frames.DefaultFloat]):
    def setup_figure(self, formatted_data: frames.DefaultFloat) -> None:
        color_scale: list[list[float | str]] = get_heatmap_colorscale()
        self.figure.add_trace(  # type: ignore
            trace=go.Heatmap(
                z=formatted_data.get_array(),
                x=formatted_data.columns,
                y=formatted_data.columns,
                showscale=False,
                colorscale=color_scale,
                hovertemplate=CustomHovers.HEATMAP.value,
            )
        )
        self.figure.update_layout(  # type: ignore
            yaxis=dict(showgrid=False, autorange="reversed")
        )
        self.figure.update_yaxes(showticklabels=False) # type: ignore
        self.figure.update_xaxes(showticklabels=False) # type: ignore
