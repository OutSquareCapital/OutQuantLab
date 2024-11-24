import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import Dashboard.Common as Common

def curves( x_values: pd.Index,
            y_values: pd.DataFrame,  
            title: str, 
            xlabel: str, 
            ylabel: str, 
            log_scale: bool = False, 
            add_zero_line: bool = False):
    
    fig = go.Figure()

    color_map = Common.get_color_map(y_values.columns)
    colors = {col: color_map[col] for col in y_values.columns}

    for column in y_values.columns:
        fig.add_trace(go.Scatter(
            x=x_values,
            y=y_values[column],
            mode='lines',
            name=column,
            line=dict(width=2, color=colors[column]),
            showlegend=True
        ))

    if add_zero_line:
        fig.add_trace(go.Scatter(
            x=x_values,
            y=[0] * len(x_values),
            mode='lines',
            name='Zero Line',
            line=dict(width=1, color='white', dash="dot"),
            showlegend=False
        ))

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(type="log" if log_scale else "linear"),
        template="plotly_dark",
        height=800
    )
    fig.show()


def bars(series: pd.Series, 
         title: str, 
         xlabel: str, 
         ylabel: str):
    
    # Générer la palette de couleurs basée sur l'index de la série
    color_map = Common.get_color_map(series.index.tolist())
    colors = [color_map[item] for item in series.index]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=series.index,
        y=series.values,
        marker_color=colors
    ))
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()


def heatmap(z_values: np.ndarray, x_labels: list, y_labels: list, title: str, colorbar_title: str):

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=x_labels.tolist(),
        y=y_labels.tolist(),
        colorscale="Jet_r",
        colorbar=dict(title=colorbar_title),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Value: %{z}<extra></extra>"
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
        template="plotly_dark",
        height=800
    )
    fig.show()


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
        ),
        template="plotly_dark",
        title=title,
        height=800
    )
    fig.show()

def treemap(labels: list, parents: list, title: str):
    fig = px.treemap(
        names=labels,
        parents=parents,
        title=title,
        template="plotly_dark",
        maxdepth=-1
    )
    fig.show()

def violin(data: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    fig = go.Figure()

    color_map = Common.get_color_map(data.columns.tolist())

    for column in data.columns:
        fig.add_trace(go.Violin(
            y=data[column],
            name=column,
            box_visible=True,
            box_line_color='white',
            points=False,
            marker=dict(color=color_map[column]),
            hoveron="violins"
        ))

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark",
        height=800
    )
    fig.show()


def ridgeline(data: pd.DataFrame, title: str, xlabel: str, ylabel: str):
    fig = go.Figure()

    color_map = Common.get_color_map(data.columns.tolist())  # Utilisation stricte de votre colormap

    for i, column in enumerate(data.columns):
        fig.add_trace(go.Violin(
            x=data[column],
            y=[i] * len(data),
            name=column,
            line_color=color_map[column],
            orientation='h',
            side='positive',
            width=1.5,
            points=False,
        ))

    # Mise à jour du layout
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(len(data.columns))),
            ticktext=data.columns.tolist(),
            showgrid=False
        ),
        xaxis=dict(showgrid=False, zeroline=False),
        template="plotly_dark",
        height=800
    )

    fig.show()
