import matplotlib.colors as mcolors
import plotly.graph_objects as go  # type: ignore
from matplotlib.colors import LinearSegmentedColormap

from outquantlab.graphs.ui_constants import Colors, TextFont


def generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    cmap_name = "custom_colormap"

    if n_colors <= len(Colors.BASE_COLORS.value):
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=Colors.BASE_COLORS.value[:n_colors], N=n_colors
        )
    else:
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=Colors.BASE_COLORS.value, N=n_colors
        )


def get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))


def map_colors_to_columns(n_colors: int) -> list[str]:
    if n_colors == 1:
        return [mcolors.to_hex(Colors.PLOT_UNIQUE.value)]
    cmap: LinearSegmentedColormap = generate_colormap(n_colors=n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]


def get_heatmap_colorscale(n_colors: int = 100):
    colormap: LinearSegmentedColormap = generate_colormap(n_colors=n_colors)
    colors: list[tuple[float, float, float, float]] = [
        colormap(i / (n_colors - 1)) for i in range(n_colors)
    ]
    return [
        [i / (n_colors - 1), mcolors.to_hex(c=color)]
        for i, color in enumerate(iterable=colors)
    ]


def setup_figure_layout(
    fig: go.Figure,
    figtitle: str,
    show_legend: bool = True,
) -> None:
    fig.update_layout(  # type: ignore
        font={
            "family": TextFont.FAMILY.value,
            "color": Colors.WHITE.value,
            "size": TextFont.TEXT_SIZE.value,
            "weight": TextFont.TYPE.value,
        },
        title={
            "text": figtitle,
            "font": {
                "size": TextFont.TITLE_SIZE.value,
                "family": TextFont.FAMILY.value,
                "weight": TextFont.TYPE.value,
            },
        },
        autosize=True,
        margin=dict(l=30, r=30, t=40, b=30),
        paper_bgcolor=Colors.BLACK.value,
        plot_bgcolor=Colors.BLACK.value,
        legend={
            "title_font": {
                "size": TextFont.LEGEND_SIZE.value,
                "family": TextFont.FAMILY.value,
                "weight": TextFont.TYPE.value,
            },
        },
    )

    fig.update_yaxes(  # type: ignore
        showgrid=False, automargin=True
    )

    fig.update_xaxes(  # type: ignore
        showgrid=False, automargin=True
    )

    if not show_legend:
        fig.update_layout(showlegend=False)  # type: ignore


def get_marker_config(color: str):
    return dict(color=color, line=dict(color=Colors.WHITE.value, width=1))


def setup_custom_hover(fig: go.Figure, hover_data: str = "y") -> None:
    for trace in fig.data:  # type: ignore
        trace.hovertemplate = f"<span style='color:{Colors.WHITE.value}'><b>%{{{hover_data}}}</b></span><extra><b>%{{fullData.name}}</b></extra>"  # type: ignore
