from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
from plotly.graph_objects import Figure
from Config import DEFAULT_TEMPLATE, DEFAULT_HEIGHT, COLOR_ADJUSTMENT
import pandas as pd
import plotly.graph_objects as go

def generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    base_colors = ["red", "yellow", "green", "lime", "blue", "cyan"]
    cmap_name = "custom_colormap"
    if n_colors == 1:
        return LinearSegmentedColormap.from_list(cmap_name, [base_colors[0], base_colors[0]], N=2)
    elif n_colors <= len(base_colors):
        return LinearSegmentedColormap.from_list(cmap_name, base_colors[:n_colors], N=n_colors)
    else:
        return LinearSegmentedColormap.from_list(cmap_name, base_colors, N=n_colors)
    
def map_colors_to_columns(n_colors: int) -> list:

    cmap = generate_colormap(n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]

def get_color_map(assets: list) -> dict:

    n_colors = len(assets)
    colors = map_colors_to_columns(n_colors)
    return dict(zip(assets, colors))

def get_heatmap_colorscale(n_colors: int = 100) -> list:
    colormap = generate_colormap(n_colors)
    colors = [colormap(i / (n_colors - 1)) for i in range(n_colors)]
    return [[i / (n_colors - 1), mcolors.to_hex(color)] for i, color in enumerate(colors)]

def setup_figure_layout(fig: Figure, 
                        title: str):
    
    fig.update_layout(
        title=title,
        template=DEFAULT_TEMPLATE,
        height=DEFAULT_HEIGHT
    )

def add_zero_line(fig: go.Figure, x_values: pd.Index):
    fig.add_trace(go.Scatter(
        x=x_values,
        y=[0] * len(x_values),
        mode='lines',
        name='Zero Line',
        line=dict(width=1, color=COLOR_ADJUSTMENT, dash="dot"),
        showlegend=False
    ))

def get_marker_config(color: str) -> dict:
    return dict(
        color=color,
        line=dict(color=COLOR_ADJUSTMENT, width=1)
    )
