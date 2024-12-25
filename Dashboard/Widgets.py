import plotly.graph_objects as go
from numpy.typing import NDArray
import pandas as pd
import numpy as np
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
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values[column],
            mode='lines',
            name=column,
            line=dict(width=2, color=color_map[column]),
            showlegend=True
        ))

    if log_scale:
        fig.update_layout(yaxis=dict(type="log"))

    setup_figure_layout(fig, title)

    return fig

def bars(
    series: pd.Series, 
    title: str
    ) -> go.Figure:
    
    color_map = get_color_map(series.index.tolist())

    fig = go.Figure()

    for item, value in series.items():
        fig.add_trace(go.Bar(
            x=[item],
            y=[value],
            name=item,
            marker=get_marker_config(color_map[item]),
            showlegend=True
        ))

    fig.update_layout(
        xaxis=dict(showticklabels=False)
    )

    setup_figure_layout(fig, title)

    return fig



def heatmap(
    z_values: NDArray[np.float32], 
    x_labels: list, 
    y_labels: list, 
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

    fig.update_layout(
        yaxis=dict(showgrid=False, autorange="reversed")
    )

    setup_figure_layout(fig, title, hover_display_custom=False)

    return fig

def scatter_3d(
    x_vals, 
    y_vals, 
    z_vals, 
    values, 
    params, 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers',
        marker=dict(
            size=8,
            color=values,
            colorscale='Jet_r',
            colorbar=dict(title="Value"),
            showscale=True
        ),
        text=['Value: {:.2f}'.format(v) for v in values],
        hovertemplate='Param1: %{x}<br>Param2: %{y}<br>Param3: %{z}<br>Value: %{marker.color}<extra></extra>'
    )])
    fig.update_layout(
        scene=dict(
            xaxis_title=params[0],
            yaxis_title=params[1],
            zaxis_title=params[2]
        )
    )

    setup_figure_layout(fig, title)
    return fig

def violin(
    data: pd.DataFrame, 
    title: str
    ) -> go.Figure:
    
    fig = go.Figure()

    color_map = get_color_map(data.columns.tolist())

    for column in data.columns:
        fig.add_trace(go.Violin(
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
    fig.update_layout(
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
        fig.add_trace(go.Histogram(
            x=data[column],
            name=column,
            marker=get_marker_config(color_map[column]),
            showlegend=True
        ))
    fig.update_layout(
        barmode="overlay"
    )
    setup_figure_layout(fig, title, hover_data='x')
    return fig

def icicle(
    labels: list, 
    parents: list, 
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