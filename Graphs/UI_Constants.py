from typing import Final

COLOR_ADJUSTMENT: Final = 'white'
COLOR_PLOT_UNIQUE: Final = '#ff6600'
BACKGROUND_APP_DARK: Final = '#2A2A2A'

FONT_FAMILY: Final = 'Arial'
FONT_SIZE: Final = 12
FONT_TYPE: Final = 'bold'
BASE_COLORS: Final = ["brown", "red","orange", "yellow", "green", "lime", "blue", "cyan"]

FIG_FONT: Final ={
            'family': FONT_FAMILY,
            'color': COLOR_ADJUSTMENT,
            'size': FONT_SIZE,
            'weight': FONT_TYPE
        }

FIG_TITLE_FONT: Final = {
                'size': FONT_SIZE*1.4, 
                'family': FONT_FAMILY,
                'weight': FONT_TYPE
                }

FIG_LEGEND_FONT: Final = {
            'title_font': {
                'size': FONT_SIZE*1.2,
                'family': FONT_FAMILY,
                'weight': FONT_TYPE
                }
        }