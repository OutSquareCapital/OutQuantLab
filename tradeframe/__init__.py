from tradeframe.categorical import FrameCategorical
from tradeframe.frames2d import FrameDated, FrameDefault, FrameMatrix
from tradeframe.frames1d import SeriesDated, SeriesNamed, SeriesDefault

__all__: list[str] = [
    "FrameCategorical",
    "FrameDated",
    "FrameDefault",
    "FrameMatrix",
    "SeriesDated",
    "SeriesNamed",
    "SeriesDefault",
]

"""
actuellement 4 types concrets:
1D avec index vertical et 1 col value vertical 
implemented avec index date, integer, ou string
2D avec index vertical et plusieurs col value verticals
implemented avec index date ou integer
Matrix avec index répété en horizontal et vertical, et values en matrice
implemented avec index string
Categorical avec value vertical, categories verticals, et colum names qui sont juste enumeration
"""