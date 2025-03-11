import plotly.graph_objects as go  # type: ignore
from outquantlab.graphs.ui_constants import Colors
from outquantlab.metrics import get_overall_max, get_overall_min
from outquantlab.typing_conventions import (
    ArrayFloat,
    DataFrameFloat,
    SeriesFloat,
)


def setup_curves(
    df: DataFrameFloat,
    color_map: dict[str, str],
) -> go.Figure:
    fig = go.Figure()
    for column in df.get_names():
        fig.add_trace(  # type: ignore
            trace=go.Scatter(
                x=df.dates,
                y=df[column],
                mode="lines",
                name=column,
                line=dict(width=2, color=color_map[column]),
            )
        )
    return fig


def setup_bars(series: SeriesFloat, color_map: dict[str, str]) -> go.Figure:
    fig = go.Figure()
    for label, value in zip(series.get_names(), series.get_array()):
        fig.add_trace(  # type: ignore
            trace=go.Bar(
                x=[label],
                y=[value],
                name=label,
                marker=_get_marker_config(color=color_map[label]),
            )
        )

    fig.update_layout(  # type: ignore
        xaxis=dict(showticklabels=False)
    )
    return fig


def setup_violin(df: DataFrameFloat, color_map: dict[str, str]) -> go.Figure:
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(  # type: ignore
            trace=go.Violin(
                y=df[column],
                name=column,
                box_visible=True,
                points=False,
                marker=_get_marker_config(color=color_map[column]),
                box_line_color=Colors.WHITE,
                hoveron="violins",
                hoverinfo="y",
            )
        )

    min_by_column: ArrayFloat = get_overall_min(array=df.get_array())
    y_min: ArrayFloat = get_overall_min(array=min_by_column)

    max_by_column: ArrayFloat = get_overall_max(array=df.get_array())
    y_max: ArrayFloat = get_overall_max(array=max_by_column)

    fig.update_layout(  # type: ignore
        yaxis=dict(range=[y_min, y_max], showgrid=False),
        xaxis=dict(
            showticklabels=False,
        ),
    )
    return fig


def setup_histogram(df: DataFrameFloat, color_map: dict[str, str]) -> go.Figure:
    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(  # type: ignore
            trace=go.Histogram(
                x=df[column],
                name=column,
                marker=_get_marker_config(color=color_map[column]),
            )
        )
    fig.update_layout(  # type: ignore
        barmode="overlay"
    )
    return fig

def setup_table(serie: SeriesFloat, color_map: dict[str, str]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(  # type: ignore
        trace=go.Table(
            header=dict(values=["Metric", "Value"], fill_color=Colors.BLACK),
            cells=dict(
                values=[serie.get_names(), serie.get_array()],
                fill_color=[color_map[name] for name in serie.get_names()],
            ),
        )
    )
    return fig

def _get_marker_config(color: str):
    return dict(color=color, line=dict(color=Colors.WHITE, width=1))

