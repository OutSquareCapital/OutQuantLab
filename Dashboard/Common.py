from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import plotly.graph_objects as go
from Files import FONT_FAMILY, FONT_SIZE, COLOR_ADJUSTMENT, BASE_COLORS, COLOR_PLOT_UNIQUE, BACKGROUND_APP_DARK
import pandas as pd

def generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    cmap_name = "custom_colormap"
    if n_colors == 1:
        return LinearSegmentedColormap.from_list(cmap_name, [BASE_COLORS[0], BASE_COLORS[0]], N=2)
    elif n_colors <= len(BASE_COLORS):
        return LinearSegmentedColormap.from_list(cmap_name, BASE_COLORS[:n_colors], N=n_colors)
    else:
        return LinearSegmentedColormap.from_list(cmap_name, BASE_COLORS, N=n_colors)
    
def map_colors_to_columns(n_colors: int) -> list:
    if n_colors == 1:
        return [mcolors.to_hex(COLOR_PLOT_UNIQUE)]
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

def setup_figure_layout(fig: go.Figure, 
                        figtitle: str):
    fig.update_layout(
        font={
            'family': FONT_FAMILY,
            'color': COLOR_ADJUSTMENT,
            'size': FONT_SIZE
        },
        title={
            'text': figtitle,
            'font': {'size': FONT_SIZE*1.4, 
                     'family': FONT_FAMILY}
        },
        autosize=True,
        margin=dict(l=30, r=30, t=40, b=30),
        paper_bgcolor=BACKGROUND_APP_DARK,
        plot_bgcolor=BACKGROUND_APP_DARK,
        legend={
            'title_font': {'size': FONT_SIZE*1.2,
                           'family': FONT_FAMILY}
        }
    )

    fig.update_yaxes(
        automargin=True,
        gridcolor=COLOR_ADJUSTMENT
    )

    fig.update_xaxes(
        showgrid=False,
        automargin=True,
        gridcolor=COLOR_ADJUSTMENT
    )

def get_marker_config(color: str) -> dict:
    return dict(
        color=color,
        line=dict(color=COLOR_ADJUSTMENT, width=1)
    )
