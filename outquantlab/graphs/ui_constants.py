from enum import Enum, StrEnum

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
    Y = f"<span style='color:{Colors.WHITE}'><b>%{{y}}</b></span><extra><b>%{{fullData.name}}</b></extra>"
    X = f"<span style='color:{Colors.WHITE}'><b>%{{x}}</b></span><extra><b>%{{fullData.name}}</b></extra>"
    HEATMAP = (
        "X: %{x}<br>Y: %{y}<br>Rank: %{z}<br>Correlation: %{customdata}<extra></extra>"
    )


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
