COLOR_ADJUSTMENT = 'white'
COLOR_PLOT_UNIQUE = '#ff6600'
BACKGROUND_APP_DARK = '#2A2A2A'

FONT_FAMILY = 'Arial'
FONT_SIZE = 12
FONT_TYPE = 'bold'
BASE_COLORS = ["black", "brown", "red","orange", "yellow", "green", "lime", "blue", "cyan", "white"]

FRAME_STYLE = f"""
        QFrame {{
            border-radius: 15px;
            background-color: {BACKGROUND_APP_DARK};
        }}
    """
CLUSTERS_PARAMETERS = [
    "Max Clusters", 
    "Max Sub Clusters", 
    "Max Sub-Sub Clusters"]
BACKTEST_STATS_RESULTS = [
    "Total Return %",
    "Sharpe Ratio",
    "Maximum Drawdown %",
    "Volatility %",
    "Monthly Skewness"]