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
