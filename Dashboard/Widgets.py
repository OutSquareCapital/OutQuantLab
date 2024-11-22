import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import Dashboard.Common as Common

def bar(fig: go.Figure, x: list, y: list, label: str, color: str, show_x_axis: bool = False):

    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name=label,
        marker_color=color
    ))
    if not show_x_axis:
        fig.update_layout(xaxis=dict(showticklabels=False))
    plt.close()

def plot_curves(data: pd.DataFrame, 
                x_values: pd.Index, 
                colors: dict, 
                title: str, 
                xlabel: str, 
                ylabel: str, 
                log_scale: bool = False, 
                add_zero_line: bool = False):
    
    fig = go.Figure()

    for column in data.columns:
        fig.add_trace(go.Scatter(
            x=x_values,
            y=data[column],
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

def histogram(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):

    df = df * 100
    # Transformation pour correspondre au format attendu par Plotly
    melted_data = df.melt(var_name='Strat', value_name='Returns')

    # Utilisation de Common pour obtenir les couleurs
    unique_assets = melted_data['Strat'].unique()
    color_map = Common.get_color_map(unique_assets)


    # Création de l'histogramme avec Plotly
    fig = px.histogram(
        melted_data,
        x='Returns',
        color='Strat',
        nbins=50,
        title=title,
        labels={'Returns': xlabel},
        opacity=0.5,
        barmode='overlay',
        color_discrete_map=color_map
    )
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template='plotly_dark',
        yaxis_type='log'  # Axe Y en échelle logarithmique
    )
    fig.show()
    plt.close()

def heatmap(z_values: np.ndarray, x_labels: list, y_labels: list, title: str, colorbar_title: str):

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale="Jet_r",  # Aligné avec la logique existante
        colorbar=dict(title=colorbar_title),
        hovertemplate="X: %{x}<br>Y: %{y}<br>Value: %{z}<extra></extra>"
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(title="X Axis", showgrid=False),
        yaxis=dict(title="Y Axis", showgrid=False, autorange="reversed"),
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
        maxdepth=-1
    )
    fig.show()

def bar_chart(data: pd.DataFrame, title: str, xlabel: str, ylabel: str, color_column: str = None):
    unique_items = data[color_column].unique() if color_column else data['x']
    color_map = Common.get_color_map(unique_items)
    colors = [color_map[item] for item in data[color_column]] if color_column else [color_map[item] for item in data['x']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['x'],
        y=data['y'],
        marker_color=colors
    ))
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()

