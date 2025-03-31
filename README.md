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
- Expandable/collapsible panels

## Requirements

### Core Dependencies

- Python 3.10+
- NumPy
- Pandas
- Plotly
- SciPy
- yfinance
- bottleneck
- polars
- pyarrow
- FastAPI

## Installation

### Clone the repository

```bash
git clone https://github.com/OutSquareCapital/OutQuantLab.git
cd OutQuantLab
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

OutQuantLab/
├── backtest/           # Backtesting process
├── config_classes/      # Select assets and indicators
├── database/          # Data handling, retrieval, and saving
├── stats/            # Statistical analysis and vizualisation
├── Indicators/        # Strategies indicators
├── metrics/          # Math and stats funcs used in indicators and stats
├── typing_conventions/ # General purposes data structures
├── web_api/          # data retrieval with yfinance, frontend web communication
└── run.py           # Entry point

## Development

### Adding New Indicators

1. Define raw calculations in `Indicators/Indics_Raw.py`
2. Add normalized version in `Indicators/Indics_Normalized.py`
3. Use the `@indic` decorator to register the indicator

### Creating new statistic measure

1. Define widget in `stats/graphs.py`
2. Implement data transformations in `stats/processors.py`
3. Instanciate the processor in `stats/main.py`
