import plotly.graph_objects as go  # type: ignore
from pandas import DatetimeIndex

from outquantlab.graphs.design import (
    get_color_map,
    get_heatmap_colorscale,
    get_marker_config,
    setup_custom_hover,
    setup_figure_layout,
)
from outquantlab.graphs.ui_constants import Colors
from outquantlab.metrics import calculate_overall_max, calculate_overall_min
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat


def curves(
    returns_df: DataFrameFloat,
    title: str,
    show_legend: bool,
    log_scale: bool = False,
) -> go.Figure:
    x_values: DatetimeIndex = returns_df.dates
    y_values: DataFrameFloat = returns_df
    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=y_values.columns.tolist())

    for column in y_values.columns:
        fig.add_trace(  # type: ignore
            trace=go.Scatter(
                x=x_values,
                y=y_values[column],
                mode="lines",
                name=column,
                line=dict(width=2, color=color_map[column]),
            )
        )

    if log_scale:
        fig.update_layout(yaxis=dict(type="log"))  # type: ignore

    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)
    setup_custom_hover(fig=fig)

    return fig


def bars(series: SeriesFloat, title: str, show_legend: bool) -> go.Figure:
    color_map: dict[str, str] = get_color_map(assets=series.names)

    fig = go.Figure()
    for label, value in zip(series.names, series.get_array()):
        fig.add_trace(  # type: ignore
            trace=go.Bar(
                x=[label],
                y=[value],
                name=label,
                marker=get_marker_config(color=color_map[label]),
            )
        )

    fig.update_layout(  # type: ignore
        xaxis=dict(showticklabels=False)
    )

    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)
    setup_custom_hover(fig=fig)
    return fig


def table(
    metrics_array: ArrayFloat,
    columns: list[str],
    rows: list[str],
    title: str,
    show_legend: bool,
) -> go.Figure:
    fig = go.Figure(
        data=go.Table(
            header=dict(values=["metrics"] + columns, fill_color="black"),
            cells=dict(
                values=[[rows[i] for i in range(len(rows))]] + metrics_array.T.tolist(),
                fill_color=[["darkblue", "darkorange"] * (len(rows) // 2 + 1)],
            ),
        )
    )
    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)
    return fig


def heatmap(
    z_values: ArrayFloat,
    x_labels: list[str],
    y_labels: list[str],
    z_normalized: ArrayFloat,
    title: str,
    show_legend: bool,
) -> go.Figure:
    colorscale = get_heatmap_colorscale()

    fig = go.Figure(
        data=go.Heatmap(
            z=z_normalized,
            x=x_labels,
            y=y_labels,
            colorscale=colorscale,
            showscale=False,
            zmin=0,
            zmax=1,
            customdata=z_values,
            hovertemplate=(
                "X: %{x}<br>"
                "Y: %{y}<br>"
                "Rank: %{z}<br>"
                "Correlation: %{customdata}<extra></extra>"
            ),
        )
    )

    fig.update_layout(  # type: ignore
        yaxis=dict(showgrid=False, autorange="reversed")
    )

    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)

    return fig


def violin(data: DataFrameFloat, title: str, show_legend: bool) -> go.Figure:
    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=data.columns.tolist())

    for column in data.columns:
        fig.add_trace(  # type: ignore
            trace=go.Violin(
                y=data[column],
                name=column,
                box_visible=True,
                points=False,
                marker=get_marker_config(color=color_map[column]),
                box_line_color=Colors.WHITE,
                hoveron="violins",
                hoverinfo="y",
            )
        )

    min_by_column: ArrayFloat = calculate_overall_min(array=data.get_array())
    y_min: ArrayFloat = calculate_overall_min(array=min_by_column)

    max_by_column: ArrayFloat = calculate_overall_max(array=data.get_array())
    y_max: ArrayFloat = calculate_overall_max(array=max_by_column)

    fig.update_layout(  # type: ignore
        yaxis=dict(range=[y_min, y_max], showgrid=False),
        xaxis=dict(
            showticklabels=False,
        ),
    )

    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)
    setup_custom_hover(fig=fig)
    return fig


def histogram(data: DataFrameFloat, title: str, show_legend: bool) -> go.Figure:
    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=data.columns.tolist())

    for column in data.columns:
        fig.add_trace(  # type: ignore
            trace=go.Histogram(
                x=data[column],
                name=column,
                marker=get_marker_config(color=color_map[column]),
            )
        )
    fig.update_layout(  # type: ignore
        barmode="overlay"
    )
    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)
    setup_custom_hover(fig=fig, hover_data="x")
    return fig


def icicle(
    labels: list[str], parents: list[str], title: str, show_legend: bool
) -> go.Figure:
    fig = go.Figure(
        data=go.Icicle(
            labels=labels,
            parents=parents,
            tiling=dict(orientation="h"),
        )
    )
    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)

    return fig
