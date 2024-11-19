
# OutQuantLab

**OutQuantLab** is a comprehensive Python framework for financial research and systematic trading strategy development. Designed with modularity, performance, and scalability in mind, it provides tools for data processing, signal generation, backtesting, portfolio management, and visualization, empowering researchers and traders to build and test complex strategies efficiently.

## Key Features

### 1. Data Processing
- **Data Retrieval and Cleaning**:
  - Import data from sources like Yahoo Finance or custom CSV files.
  - Clean and normalize data with advanced methods like rolling normalization and risk-free rate adjustments.
- **Dynamic and Static Structuring**:
  - Categorize assets into flexible hierarchies (e.g., ratios, ensembles) for systematic portfolio management.
  - Generate continuous price series and adjust for contract rollovers.

### 2. Signal Generation
- **Raw and Normalized Signals**:
  - Implements a wide variety of trading signals, including trend, momentum, mean reversion, and seasonality-based indicators.
  - Supports advanced techniques like MACD-style acceleration metrics and rolling skewness/kurtosis analysis.
- **Adaptive Normalization**:
  - Apply trend-based conditioning, rolling median normalization, and volatility-based adjustments to optimize signals.

### 3. Backtesting
- **Automated Parameter Generation**:
  - Define flexible parameter ranges and automatically generate combinations for extensive strategy testing.
- **Signal Processing**:
  - Process trading signals with advanced volatility adjustments and long/short bias corrections.
- **Performance Metrics**:
  - Evaluate strategies with rolling Sharpe ratios, Sortino ratios, and other risk-adjusted metrics.

### 4. Portfolio Management
- **Weighting and Clustering**:
  - Generate static and dynamic weights for assets, adjusting for availability and volatility.
  - Perform hierarchical clustering of assets based on correlation or custom metrics.
- **Trading Cost Analysis**:
  - Integrate transaction cost modeling to ensure realistic performance evaluations.

### 5. Visualization and Reporting
- **Comprehensive Dashboards**:
  - Visualize equity curves, drawdowns, rolling Sharpe ratios, and correlation heatmaps.
- **3D and Heatmap Analysis**:
  - Explore parameter impacts using 3D scatter plots and Sharpe ratio heatmaps.
- **Customizable Reporting**:
  - Generate detailed visual insights to evaluate strategy performance across multiple dimensions.

## Architecture Overview

OutQuantLab is structured into several interdependent modules, each focusing on a specific area of quantitative research:

1. **Data**:
   - Handles all aspects of data ingestion, cleaning, and organization.

2. **Signals**:
   - Focuses on the generation and normalization of trading signals.

3. **Backtest**:
   - Provides tools for parameter generation, signal processing, and strategy evaluation.

4. **Portfolio**:
   - Enables portfolio construction, clustering, and dynamic weight adjustments.

5. **Dashboard**:
   - Offers a suite of visualization tools to analyze and present strategy performance.

## Workflow Example

### Step 1: Define Indicators and Parameters
```python
methods = [
    Trend.mean_price_ratio,
    Volatility.relative_directional_volatility,
]
param_options = {
    'Trend': {'LenST': Backtest.param_range_values(4, 64, 5), 'LenLT': Backtest.param_range_values(16, 256, 5)},
    'Volatility': {'LenVol': Backtest.param_range_values(4, 256, 7)},
}
indicators_and_params = Backtest.automatic_generation(methods, param_options)
```

### Step 2: Load and Process Data
```python
data_prices_df, assets_names = Data.load_prices_from_csv(Config.file_path_yf)
processed_data = Data.process_category_data(assets_names, data_prices_df, initial_equity=100)
```

### Step 3: Generate Trading Signals
```python
signals_df, raw_adjusted_returns_df = Backtest.SignalsProcessing.trading_signals(
    processed_data['returnstreams']['prices_array'],
    processed_data['returnstreams']['log_returns_array'],
    processed_data['returnstreams']['log_returns_df'],
    processed_data['returnstreams']['pct_returns_array'],
    processed_data['returnstreams']['hv_array'],
    processed_data['returnstreams']['asset_names'],
    indicators_and_params
)
```

### Step 4: Portfolio Management and Optimization
```python
portfolio_structure = Portfolio.classify_assets(processed_data['returnstreams']['asset_names'], Config.portfolio_etf)
```

### Step 5: Visualization
```python
Dashboard.equity(Data.equity_curves_calculs(raw_adjusted_returns_df, initial_equity=100000))
```

## System Requirements
- **Python**: >= 3.8
- **Libraries**: NumPy, pandas, Numba, Bottleneck, Matplotlib, Plotly, Scipy

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/OutQuantLab.git
   cd OutQuantLab
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main workflow to build and evaluate strategies.

OutQuantLab is a powerful, flexible tool for advanced quantitative research and trading strategy development. Its modular design allows users to explore a wide range of financial models, optimize portfolios, and generate meaningful insights through detailed visualization.
