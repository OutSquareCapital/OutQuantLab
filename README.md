# OutQuantLab

OutQuantLab is a comprehensive Python-based quantitative analysis platform for backtesting systematic trading strategies, with emphasis on technical indicators and clustering analysis.

## Key Features

### Trading Strategy Analysis
- Multi-threaded backtesting engine
- Extensive library of technical indicators:
  - Moving averages (mean, median, central)
  - Momentum indicators
  - Volatility-based indicators
  - Advanced statistics (skewness, kurtosis)
- Performance metrics and risk analysis

### Data Management
- Integration with Yahoo Finance
- Custom DataFrame types optimized for financial data
- Local data storage in Parquet format
- Efficient data processing with NumPy/Pandas

### Advanced Analytics
- Dynamic asset clustering
- Correlation analysis
- Distribution analysis
- Volatility normalization
- Multi-level hierarchical organization

### Visualization
- Interactive equity curves
- Performance metrics dashboards
- Distribution plots (violin, histogram)
- Correlation heatmaps
- Hierarchical clustering visualization
- Custom color schemes

### User Interface
- Full-featured GUI built with PySide6
- Command-line interface
- Interactive parameter configuration
- Real-time progress tracking
- Expandable/collapsible panels

## Requirements

### Core Dependencies
- Python 3.10+
- NumPy
- Pandas
- Plotly
- PySide6
- SciPy
- yfinance
- bottleneck
- polars
- pyarrow

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OutSquareCapital/OutQuantLab.git
cd OutQuantLab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
OutQuantLab/
├── App/                 # Application core
├── Backtest/           # Backtesting engine
├── ConfigClasses/      # Configuration management
├── DataBase/          # Data handling
├── Graphs/            # Visualization tools
├── Indicators/        # Technical indicators
├── metrics/          # Performance metrics
├── UI/               # User interface
├── Utilitary/        # Utility functions
└── Run.py           # Entry point
```

## Development

### Adding New Indicators

1. Define raw calculations in `Indicators/Indics_Raw.py`
2. Add normalized version in `Indicators/Indics_Normalized.py`
3. Use the `@indic` decorator to register the indicator

### Creating Visualization Widgets

1. Define widget in `Graphs/Widgets.py`
2. Add color scheme in `Graphs/Design.py`
3. Implement data transformations in `Graphs/Transformations.py`