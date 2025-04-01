from enum import Enum, StrEnum

import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

BASE_COLORS: list[str] = [
    "brown",
    "red",
    "orange",
    "yellow",
    "green",
    "lime",
    "blue",
    "cyan",
]


class Colors(StrEnum):
    WHITE = "white"
    BLACK = "#2A2A2A"
    PLOT_UNIQUE = "#ff6600"


class TextFont(StrEnum):
    FAMILY = "Arial"
    TYPE = "bold"


class TextSize(Enum):
    STANDARD = 12
    TITLE = 17
    LEGEND = 14


class CustomHovers(Enum):
    VERTICAL_DATA = f"<span style='color:{Colors.WHITE}'><b>%{{y}}</b></span><extra><b>%{{fullData.name}}</b></extra>"
    HORIZONTAL_DATA = f"<span style='color:{Colors.WHITE}'><b>%{{x}}</b></span><extra><b>%{{fullData.name}}</b></extra>"
    HEATMAP = "X: %{x}<br>Y: %{y}<br>Correlation: %{z}<extra></extra>"


class FigureSetup(Enum):
    TEXT_FONT = {
        "family": TextFont.FAMILY,
        "color": Colors.WHITE,
        "size": TextSize.STANDARD.value,
        "weight": TextFont.TYPE,
    }

    TITLE_FONT = {
        "size": TextSize.TITLE.value,
        "family": TextFont.FAMILY,
        "weight": TextFont.TYPE,
    }

    LEGEND_TITLE_FONT = {
        "size": TextSize.LEGEND.value,
        "family": TextFont.FAMILY,
        "weight": TextFont.TYPE,
    }


def get_marker_config(color: str) -> dict[str, str | dict[str, Colors | int]]:
    return dict(color=color, line=dict(color=Colors.WHITE, width=1))


def get_color_map(assets: list[str]) -> dict[str, str]:
    n_colors: int = len(assets)
    colors: list[str] = _map_colors_to_columns(n_colors=n_colors)
    return dict(zip(assets, colors))


def get_heatmap_colorscale(n_colors: int = 100) -> list[list[float | str]]:
    colormap: LinearSegmentedColormap = _generate_colormap(n_colors=n_colors)

    colors: list[tuple[float, float, float, float]] = [
        colormap(i / (n_colors - 1)) for i in range(n_colors)
    ]

    return [
        [i / (n_colors - 1), mcolors.to_hex(c=color)]
        for i, color in enumerate(iterable=colors)
    ]


def _map_colors_to_columns(n_colors: int) -> list[str]:
    if n_colors == 1:
        return [mcolors.to_hex(Colors.PLOT_UNIQUE.value)]
    cmap: LinearSegmentedColormap = _generate_colormap(n_colors=n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]


def _generate_colormap(n_colors: int) -> LinearSegmentedColormap:
    cmap_name = "custom_colormap"

    if n_colors <= len(BASE_COLORS):
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=BASE_COLORS[:n_colors], N=n_colors
        )
    else:
        return LinearSegmentedColormap.from_list(
            name=cmap_name, colors=BASE_COLORS, N=n_colors
        )
