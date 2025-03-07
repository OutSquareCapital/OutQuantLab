import plotly.graph_objects as go  # type: ignore
from pandas import DatetimeIndex
from numpy import nanmax, nanmin, zeros_like
from outquantlab.graphs.design import (
    get_color_map,
    get_heatmap_colorscale,
    get_marker_config,
    setup_custom_hover,
    setup_figure_layout,
)
from outquantlab.graphs.ui_constants import Colors
from outquantlab.metrics import get_overall_max, get_overall_min
from outquantlab.typing_conventions import (
    ArrayFloat,
    DataFrameFloat,
    SeriesFloat,
    Float32,
)


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
    returns_df: DataFrameFloat,
    title: str,
    show_legend: bool,
) -> go.Figure:
    colorscale: list[list[float | str]] = get_heatmap_colorscale()
    corr_matrix_normalised = _normalize_data_for_colormap(data=returns_df.get_array())
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix_normalised,
            x=returns_df.columns,
            y=returns_df.columns,
            colorscale=colorscale,
            showscale=False,
            zmin=0,
            zmax=1,
            customdata=returns_df.get_array(),
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

    min_by_column: ArrayFloat = get_overall_min(array=data.get_array())
    y_min: ArrayFloat = get_overall_min(array=min_by_column)

    max_by_column: ArrayFloat = get_overall_max(array=data.get_array())
    y_max: ArrayFloat = get_overall_max(array=max_by_column)

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
    clusters_dict: dict[str, list[str]], title: str, show_legend: bool
) -> go.Figure:
    labels, parents = _prepare_sunburst_data(cluster_dict=clusters_dict)
    fig = go.Figure(
        data=go.Icicle(
            labels=labels,
            parents=parents,
            tiling=dict(orientation="h"),
        )
    )
    setup_figure_layout(fig=fig, figtitle=title, show_legend=show_legend)

    return fig


def _normalize_data_for_colormap(data: ArrayFloat) -> ArrayFloat:
    z_min: Float32 = nanmin(data)
    z_max: Float32 = nanmax(data)
    return (
        (data - z_min) / (z_max - z_min)
        if z_max > z_min
        else zeros_like(a=data, dtype=Float32)
    )


def _prepare_sunburst_data(
    cluster_dict: dict[str, list[str]],
    parent_label: str = "",
    labels: list[str] | None = None,
    parents: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    if labels is None:
        labels = []
    if parents is None:
        parents = []

    for key, value in cluster_dict.items():
        current_label: str = parent_label + str(key) if parent_label else str(key)
        if isinstance(value, dict):
            _prepare_sunburst_data(
                cluster_dict=value,
                parent_label=current_label,
                labels=labels,
                parents=parents,
            )
        else:
            for asset in value:
                labels.append(asset)
                parents.append(current_label)
        if parent_label:
            labels.append(current_label)
            parents.append(parent_label)
        else:
            labels.append(current_label)
            parents.append("")

    return labels, parents
