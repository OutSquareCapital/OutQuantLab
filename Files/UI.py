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

ROLLING_BUTTONS_NAMES = [
    "Equity", 
    "Sharpe Ratio", 
    "Drawdown", 
    "Volatility", 
    "Smoothed Skewness", 
    "Average Inverted Correlation"]
OVERALL_BUTTONS_NAMES = [
    "Total Returns %",
    "Overall Sharpe Ratio",
    "Average Drawdown", 
    "Overall Volatility", 
    "Monthly Skew",
    "Overall Average Decorrelation"]
ADVANCED_BUTTONS_NAMES = [
    "Correlation Heatmap", 
    "Clusters Icicle", 
    "Distribution Histogram", 
    "Distribution Violin"]
CLUSTERS_PARAMETERS = [
    "Max Clusters", 
    "Max Sub Clusters", 
    "Max Sub-Sub Clusters"]
BACKTEST_STATS_RESULTS = [
    "Total Return %",
    "Sharpe Ratio",
    "Average Drawdown %",
    "Volatility %",
    "Monthly Skewness"]