import plotly.graph_objects as go # type: ignore
from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat
import pandas as pd
from Dashboard.Common import get_color_map, get_heatmap_colorscale, setup_figure_layout, get_marker_config
from Dashboard.Transformations import normalize_data_for_colormap
from Utilitary import COLOR_ADJUSTMENT
from Metrics import calculate_overall_max, calculate_overall_min

def curves( x_values: pd.DatetimeIndex,
            y_values: DataFrameFloat,  
            title: str,
            log_scale: bool = False
            ) -> go.Figure:

    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=y_values.columns.tolist())

    for column in y_values.columns:
        fig.add_trace(trace=go.Scatter( # type: ignore
            x=x_values,
            y=y_values[column],
            mode='lines',
            name=column,
            line=dict(width=2, color=color_map[column]),
            showlegend=True
        ))

    if log_scale:
        fig.update_layout(yaxis=dict(type="log")) # type: ignore

    setup_figure_layout(fig=fig, figtitle=title)

    return fig

def bars(
    series: SeriesFloat, 
    title: str
    ) -> go.Figure:

    color_map: dict[str, str] = get_color_map(assets=series.names)

    fig = go.Figure()
    for label, value in zip(series.names, series.nparray):
        fig.add_trace(trace=go.Bar( # type: ignore
            x=[label],
            y=[value],
            name=label,
            marker=get_marker_config(color=color_map[label]),
            showlegend=True
        ))

    fig.update_layout( # type: ignore
        xaxis=dict(showticklabels=False)
    )

    setup_figure_layout(fig=fig, figtitle=title)

    return fig


def heatmap(
    z_values: ArrayFloat, 
    x_labels: list[str], 
    y_labels: list[str], 
    title: str
    ) -> go.Figure:

    z_normalized = normalize_data_for_colormap(data=z_values)

    colorscale = get_heatmap_colorscale()

    fig = go.Figure(data=go.Heatmap(
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
    )
    ))

    fig.update_layout( # type: ignore
        yaxis=dict(showgrid=False, autorange="reversed")
    )

    setup_figure_layout(fig=fig, figtitle=title, hover_display_custom=False)

    return fig

def violin(
    data: DataFrameFloat, 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=data.columns.tolist())

    for column in data.columns:
        fig.add_trace(trace=go.Violin( # type: ignore
            y=data[column],
            name=column,
            box_visible=True,
            points=False,
            marker=get_marker_config(color=color_map[column]),
            box_line_color=COLOR_ADJUSTMENT,
            hoveron="violins",
            hoverinfo="y" 
        ))

    min_by_column: ArrayFloat = calculate_overall_min(array=data.nparray)
    y_min: ArrayFloat = calculate_overall_min(array=min_by_column)
    
    max_by_column: ArrayFloat = calculate_overall_max(array=data.nparray)
    y_max: ArrayFloat = calculate_overall_max(array=max_by_column)

    fig.update_layout( # type: ignore
        yaxis=dict(range=[y_min, y_max], showgrid=False), 
        xaxis=dict(
            showticklabels=False,
            )
        )

    setup_figure_layout(fig, figtitle=title)

    return fig

def histogram(
    data: DataFrameFloat, 
    title: str
    ) -> go.Figure:

    fig = go.Figure()

    color_map: dict[str, str] = get_color_map(assets=data.columns.tolist())

    for column in data.columns:
        fig.add_trace(trace=go.Histogram( # type: ignore
            x=data[column],
            name=column,
            marker=get_marker_config(color=color_map[column]),
            showlegend=True
        ))
    fig.update_layout( # type: ignore
        barmode="overlay"
    )
    setup_figure_layout(fig=fig, figtitle=title, hover_data='x')
    return fig

def icicle(
    labels: list[str], 
    parents: list[str], 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure(
        data=go.Icicle(
            labels=labels,            
            parents=parents,          
            tiling=dict(orientation="v"),
        )
    )
    setup_figure_layout(fig=fig, figtitle=title, hover_display_custom=False)
    
    return fig