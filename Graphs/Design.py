from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
import plotly.graph_objects as go # type: ignore
from Utilitary import COLOR_ADJUSTMENT, BASE_COLORS, COLOR_PLOT_UNIQUE, BACKGROUND_APP_DARK, FIG_FONT, FIG_LEGEND_FONT, FIG_TITLE_FONT

def determine_category(name: str) -> str:
    if "overall" in name:
        return "overall"
    elif "rolling" in name:
        return "rolling"
    else:
        return "other"

def generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    cmap_name = "custom_colormap"
    if n_colors == 1:
        return LinearSegmentedColormap.from_list(name=cmap_name, colors=[BASE_COLORS[0], BASE_COLORS[0]], N=2)
    elif n_colors <= len(BASE_COLORS):
        return LinearSegmentedColormap.from_list(name=cmap_name, colors=BASE_COLORS[:n_colors], N=n_colors)
    else:
        return LinearSegmentedColormap.from_list(name=cmap_name, colors=BASE_COLORS, N=n_colors)
    
def map_colors_to_columns(n_colors: int) -> list[str]:
    if n_colors == 1:
        return [mcolors.to_hex(COLOR_PLOT_UNIQUE)]
    cmap: LinearSegmentedColormap = generate_colormap(n_colors=n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]

def get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))

def get_heatmap_colorscale(n_colors: int = 100):
    colormap: LinearSegmentedColormap = generate_colormap(n_colors=n_colors)
    colors: list[tuple[float, float, float, float]] = [colormap(i / (n_colors - 1)) for i in range(n_colors)]
    return [[i / (n_colors - 1), mcolors.to_hex(c=color)] for i, color in enumerate(iterable=colors)]

def setup_figure_layout(
    fig: go.Figure, 
    figtitle: str,
    hover_display_custom: bool=True,
    hover_data: str ='y',
    show_legend: bool = True) -> None:
    
    fig.update_layout( # type: ignore
        font=FIG_FONT,
        title={
            'text': figtitle,
            'font': FIG_TITLE_FONT
        },
        autosize=True,
        margin=dict(l=30, r=30, t=40, b=30),
        paper_bgcolor=BACKGROUND_APP_DARK,
        plot_bgcolor=BACKGROUND_APP_DARK,
        legend=FIG_LEGEND_FONT
    )

    fig.update_yaxes( # type: ignore
        showgrid=False,
        automargin=True
    )

    fig.update_xaxes( # type: ignore
        showgrid=False,
        automargin=True
    )
    if hover_display_custom:
        
        for trace in fig.data: # type: ignore
            trace.hovertemplate = f"<span style='color:{COLOR_ADJUSTMENT}'><b>%{{{hover_data}}}</b></span><extra><b>%{{fullData.name}}</b></extra>" # type: ignore

    if not show_legend:
        fig.update_layout(showlegend=False) # type: ignore

def get_marker_config(color:str):
    return dict(
        color=color,
        line=dict(color=COLOR_ADJUSTMENT, width=1)
    )
