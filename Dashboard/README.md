
# Dashboard

**Dashboard** is a modular and extensible Python package designed for analyzing, visualizing, and interpreting financial data and trading strategies. It integrates features for computation, interactive visualization, and performance analysis.

## Key Features

- **Advanced Calculations**:
  - Performance metrics such as Sharpe, Sortino, and Skew ratios.
  - Drawdown analysis and annual/monthly returns.
  - Parameter sensitivity analysis for strategies.
  - Combined metrics like Sharpe/Avg Correlation.

- **Interactive Visualizations**:
  - Equity curves and return distribution histograms.
  - Correlation heatmaps and 3D surfaces for parameter optimization.
  - Static cluster visualizations using treemap/sunburst.

- **Customizable Graphs**:
  - Dynamic colormaps for multi-strategy visualizations.
  - Colored tables and interactive graphs with `Plotly`.

## Example Usage

### Strategy Analysis

```python
import pandas as pd
from Dashboard import Display, Computations

# Load daily returns data
daily_returns = pd.read_csv('daily_returns.csv', index_col=0, parse_dates=True)

# Calculate and display Sharpe ratios
sharpe_ratios = Computations.overall_sharpe_ratios_calculs(daily_returns)
Display.overall_sharpe_ratios(daily_returns)
```

### 3D Visualization

```python
Display.sharpe_ratios_3d_surface_plot(daily_returns, param1='ZScoreLength', param2='PercentileLength')
```

## Modules

1. **`Common`**:
   - Utility functions for grid calculations, custom colormaps, and parameter extraction from strategy names.

2. **`Computations`**:
   - Functions for performance metrics calculations, correlations, and parameter analyses.

3. **`Display`**:
   - Visualization module using `Plotly` and `Matplotlib` for interactive performance graphs and visual analytics.

4. **`Selection`** and **`Widgets`**:
   - Functions for creating modular and interactive tables and plots.

### Initialization File

The `__init__.py` file automatically imports the key modules for simplified access.

```python
from .Display import *
```
