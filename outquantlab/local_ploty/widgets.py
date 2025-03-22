import matplotlib.colors as mcolors
import plotly.graph_objects as go  # type: ignore
from matplotlib.colors import LinearSegmentedColormap

import outquantlab.metrics as mt
from outquantlab.local_ploty.graph_class import Graph
from outquantlab.local_ploty.ui_constants import BASE_COLORS, Colors, CustomHovers
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat


class Curves(Graph[DataFrameFloat]):
    def _setup_figure_type(self, formatted_data: DataFrameFloat) -> None:
        color_map: dict[str, str] = _get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Scatter(
                    x=formatted_data.dates,
                    y=formatted_data[column],
                    mode="lines",
                    name=column,
                    line=dict(width=2, color=color_map[column]),
                    hovertemplate=CustomHovers.Y.value,
                )
            )


class Violins(Graph[DataFrameFloat]):
    def _setup_figure_type(self, formatted_data: DataFrameFloat) -> None:
        color_map: dict[str, str] = _get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Violin(
                    y=formatted_data[column],
                    name=column,
                    box_visible=True,
                    points=False,
                    marker=_get_marker_config(color=color_map[column]),
                    box_line_color=Colors.WHITE,
                    hoveron="violins",
                    hoverinfo="y",
                    hovertemplate=CustomHovers.Y.value,
                )
            )

        min_by_column: ArrayFloat = mt.get_overall_min(array=formatted_data.get_array())
        y_min: ArrayFloat = mt.get_overall_min(array=min_by_column)

        max_by_column: ArrayFloat = mt.get_overall_max(array=formatted_data.get_array())
        y_max: ArrayFloat = mt.get_overall_max(array=max_by_column)

        self.figure.update_layout(  # type: ignore
            yaxis=dict(range=[y_min, y_max], showgrid=False),
            xaxis=dict(
                showticklabels=False,
            ),
        )


class Histogram(Graph[DataFrameFloat]):
    def _setup_figure_type(self, formatted_data: DataFrameFloat) -> None:
        color_map: dict[str, str] = _get_color_map(assets=formatted_data.get_names())
        for column in formatted_data.columns:
            self.figure.add_trace(  # type: ignore
                trace=go.Histogram(
                    x=formatted_data[column],
                    name=column,
                    marker=_get_marker_config(color=color_map[column]),
                    hovertemplate=CustomHovers.X.value,
                )
            )
        self.figure.update_layout(  # type: ignore
            barmode="overlay"
        )


class Bars(Graph[SeriesFloat]):
    def _setup_figure_type(self, formatted_data: SeriesFloat) -> None:
        color_map: dict[str, str] = _get_color_map(assets=formatted_data.get_names())
        for label, value in zip(
            formatted_data.get_names(),
            formatted_data.get_array(),
        ):
            self.figure.add_trace(  # type: ignore
                trace=go.Bar(
                    x=[label],
                    y=[value],
                    name=label,
                    marker=_get_marker_config(color=color_map[label]),
                    hovertemplate=CustomHovers.Y.value,
                )
            )

        self.figure.update_layout(  # type: ignore
            xaxis=dict(showticklabels=False)
        )


class Table(Graph[SeriesFloat]):
    def _setup_figure_type(self, formatted_data: SeriesFloat) -> None:
        self.figure.add_trace(  # type: ignore
            trace=go.Table(
                header=dict(values=["Metric", "Value"], fill_color=Colors.BLACK),
                cells=dict(
                    values=[
                        formatted_data.get_names(),
                        formatted_data.get_array(),
                    ],
                    fill_color=[Colors.PLOT_UNIQUE],
                ),
            )
        )


class HeatMap(Graph[DataFrameFloat]):
    def _setup_figure_type(self, formatted_data: DataFrameFloat) -> None:
        color_scale: list[list[float | str]] = get_heatmap_colorscale()
        self.figure.add_trace( # type: ignore
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


def _get_marker_config(color: str) -> dict[str, str | dict[str, Colors | int]]:
    return dict(color=color, line=dict(color=Colors.WHITE, width=1))


def _get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = _map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))


def get_heatmap_colorscale(n_colors: int = 100):
    colormap: LinearSegmentedColormap = _generate_colormap(n_colors=n_colors)

    colors: list[tuple[float, float, float, float]] = [
        colormap(i / (n_colors - 1)) for i in range(n_colors)
    ]

    return [
        [i / (n_colors - 1), mcolors.to_hex(c=color)]
        for i, color in enumerate(iterable=colors)
    ]


def _map_colors_to_columns(n_colors: int) -> list[str]:
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
