from enum import Enum
class Colors(Enum):
    BASE_COLORS= ["brown", "red", "orange", "yellow", "green", "lime", "blue", "cyan"]
    WHITE = "white"
    BLACK = "#2A2A2A"
    PLOT_UNIQUE = '#ff6600'


class TextFont(Enum):
    FAMILY = "Arial"
    TEXT_SIZE = 12
    TITLE_SIZE = 17
    LEGEND_SIZE = 14
    TYPE = "bold"
