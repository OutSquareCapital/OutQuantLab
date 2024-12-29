from typing import Final

COLOR_ADJUSTMENT: Final = 'white'
COLOR_PLOT_UNIQUE: Final = '#ff6600'
BACKGROUND_APP_DARK: Final = '#2A2A2A'

FONT_FAMILY: Final = 'Arial'
FONT_SIZE: Final = 12
FONT_TYPE: Final = 'bold'
BASE_COLORS: Final = ["black", "brown", "red","orange", "yellow", "green", "lime", "blue", "cyan", "white"]

FRAME_STYLE: Final = f"""
        QFrame {{
            border-radius: 15px;
            background-color: {BACKGROUND_APP_DARK};
        }}
    """
CLUSTERS_PARAMETERS: Final = [
    "Max Clusters", 
    "Max Sub Clusters", 
    "Max Sub-Sub Clusters"
    ]