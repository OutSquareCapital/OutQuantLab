import plotly.graph_objects as go # type: ignore
from Files import NDArrayFloat
import pandas as pd
from Dashboard.Common import get_color_map, get_heatmap_colorscale, setup_figure_layout, get_marker_config
from .Transformations import normalize_data_for_colormap
from Files import COLOR_ADJUSTMENT

def curves( x_values: pd.Index,
            y_values: pd.DataFrame,  
            title: str,
            log_scale: bool = False
            ) -> go.Figure:

    fig = go.Figure()

    color_map = get_color_map(y_values.columns.tolist())

    for column in y_values.columns:
        fig.add_trace(go.Scatter( # type: ignore
            x=x_values,
            y=y_values[column],
            mode='lines',
            name=column,
            line=dict(width=2, color=color_map[column]),
            showlegend=True
        ))

    if log_scale:
        fig.update_layout(yaxis=dict(type="log")) # type: ignore

    setup_figure_layout(fig, title)

    return fig

def bars(
    series: pd.Series, 
    title: str
    ) -> go.Figure:
    
    index: pd.Index[str] = series.index # type: ignore

    color_map = get_color_map(index.tolist())

    fig = go.Figure()

    for item, value in series.items():
        fig.add_trace(go.Bar( # type: ignore
            x=[item],
            y=[value],
            name=item,
            marker=get_marker_config(color_map[item]), # type: ignore
            showlegend=True
        ))

    fig.update_layout( # type: ignore
        xaxis=dict(showticklabels=False)
    )

    setup_figure_layout(fig, title)

    return fig



def heatmap(
    z_values: NDArrayFloat, 
    x_labels: list[str], 
    y_labels: list[str], 
    title: str
    ) -> go.Figure:

    z_normalized = normalize_data_for_colormap(z_values)

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

    setup_figure_layout(fig, title, hover_display_custom=False)

    return fig

def violin(
    data: pd.DataFrame, 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure()

    color_map = get_color_map(data.columns.tolist())

    for column in data.columns:
        fig.add_trace(go.Violin( # type: ignore
            y=data[column],
            name=column,
            box_visible=True,
            points=False,
            marker=get_marker_config(color_map[column]),
            box_line_color=COLOR_ADJUSTMENT,
            hoveron="violins",
            hoverinfo="y" 
        ))

    y_min = data.min().min()
    y_max = data.max().max()
    fig.update_layout( # type: ignore
        yaxis=dict(range=[y_min, y_max], showgrid=False),
        xaxis=dict(
            showticklabels=False,
            )
        )
    
    setup_figure_layout(fig, title)

    return fig

def histogram(
    data: pd.DataFrame, 
    title: str
    ) -> go.Figure:

    fig = go.Figure()

    color_map = get_color_map(data.columns.tolist())

    for column in data.columns:
        fig.add_trace(go.Histogram( # type: ignore
            x=data[column],
            name=column,
            marker=get_marker_config(color_map[column]),
            showlegend=True
        ))
    fig.update_layout( # type: ignore
        barmode="overlay"
    )
    setup_figure_layout(fig, title, hover_data='x')
    return fig

def icicle(
    labels: list[str], 
    parents: list[str], 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure(
        go.Icicle(
            labels=labels,            
            parents=parents,          
            tiling=dict(orientation="v"),
        )
    )
    setup_figure_layout(fig, title, hover_display_custom=False)
    
    return fig