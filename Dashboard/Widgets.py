import plotly.graph_objects as go
import pandas as pd
import numpy as np
from Dashboard.Common import get_color_map, get_heatmap_colorscale, setup_figure_layout, add_zero_line, get_marker_config
import Dashboard.Transformations as Transformations
from Config import COLOR_ADJUSTMENT

def curves( x_values: pd.Index,
            y_values: pd.DataFrame,  
            title: str,
            xlabel: str,
            ylabel: str,
            log_scale: bool = False, 
            zero_line: bool = False):

    fig = go.Figure()

    color_map = get_color_map(y_values.columns)

    for column in y_values.columns:
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values[column],
            mode='lines',
            name=column,
            line=dict(width=2, color=color_map[column]),
            showlegend=True
        ))

    if zero_line:
        add_zero_line(fig, x_values)

    if log_scale:
        fig.update_layout(yaxis=dict(type="log"))

    fig.update_layout(       
        xaxis_title=xlabel,
        yaxis_title=ylabel
        )
    
    setup_figure_layout(fig, title)

    return fig

def bars(series: pd.Series, title: str, xlabel: str, ylabel: str):
    # Gestion des couleurs avec votre méthode
    color_map = get_color_map(series.index.tolist())

    fig = go.Figure()

    for item, value in series.items():
        fig.add_trace(go.Bar(
            x=[item],
            y=[value],
            name=item,
            marker=get_marker_config(color_map[item]),
            showlegend=True,
            hovertemplate=f"<b>{item}</b><br>Value: {value:.2f}<extra></extra>"
        ))

    # Configuration générale du graphique
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        xaxis=dict(showticklabels=False),
        showlegend=True
    )

    setup_figure_layout(fig, title)

    return fig



def heatmap(z_values: np.ndarray, x_labels: list, y_labels: list, title: str):

    z_normalized = Transformations.normalize_data_for_colormap(z_values)

    colorscale = get_heatmap_colorscale()

    fig = go.Figure(data=go.Heatmap(
        z=z_normalized,
        x=x_labels,
        y=y_labels,
        colorscale=colorscale,
        showscale=False,
        zmin=0,
        zmax=1,
        hovertemplate="X: %{x}<br>Y: %{y}<br>Value: %{customdata}<extra></extra>",
        customdata=z_values
    ))
    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, autorange="reversed")
    )

    setup_figure_layout(fig, title)

    return fig

def scatter_3d(x_vals, y_vals, z_vals, values, params, title: str):
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

def violin(data: pd.DataFrame, title: str, xlabel: str, ylabel: str):
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
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(range=[y_min, y_max], showgrid=False),
        xaxis=dict(
            showticklabels=False,
            showgrid=False
            )
        )
    
    setup_figure_layout(fig, title)

    return fig

def histogram(data: pd.DataFrame, title: str, xlabel: str, ylabel: str):

    fig = go.Figure()

    color_map = get_color_map(data.columns.tolist())

    for column in data.columns:
        fig.add_trace(go.Histogram(
            x=data[column],
            name=column,
            marker=get_marker_config(color_map[column]),
            hoverinfo="y",
            showlegend=True
        ))
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        barmode="overlay"
    )
    setup_figure_layout(fig,  title)
    return fig

def icicle(labels: list, parents: list, title: str):
    fig = go.Figure(
        go.Icicle(
            labels=labels,            
            parents=parents,          
            tiling=dict(orientation="v"),
        )
    )
    setup_figure_layout(fig, title)
    
    return fig