
# Data

**Data** is a Python package designed to handle the entire lifecycle of financial data processing, including retrieval, cleaning, transformation, and organization. It emphasizes scalability, flexibility, and accuracy for use in financial research and analysis.

## Key Functionalities

### 1. Data Retrieval
- **Integration with Yahoo Finance**: Fetch financial data directly from Yahoo Finance and save it in a structured format for further processing.
- **Custom Data Loading**: Load datasets from various sources, including preformatted CSV files, while ensuring compatibility with the package's internal structure.

### 2. Data Cleaning
- **Negative Price Adjustment**: Automatically corrects negative values in price series to ensure data consistency.
- **Handling Missing Data**: Reconstructs missing values in price data using forward-fill and random sampling methods, ensuring continuity without introducing bias.
- **Standardization**: Adjusts and inverts specific asset classes (e.g., volatility indices) for standardization with other asset types.

### 3. Data Transformation
- **Return Calculations**: Compute percentage and logarithmic returns from raw price data for use in strategy development and analysis.
- **Volatility Adjusted Returns**: Transform returns based on historical volatility to normalize risk exposure.
- **Equity Curve Construction**: Generate equity curves from returns, ensuring smooth integration into backtesting workflows.

### 4. Data Organization
- **Category Grouping**: Dynamically group assets into categories like ratios, ensembles, and canary assets for structured analysis.
- **Combination and Recombination**: Merge, split, and recombine categories into unified datasets for use in modeling and simulations.
- **Ratio and Ensemble Calculations**: Generate custom metrics and aggregated returns based on user-defined combinations of assets.

### Modules

1. **`Get_Data`**:
   - Functions for downloading data from external sources and loading pre-saved datasets into the pipeline.

2. **`Clean_Data`**:
   - Tools for addressing data quality issues such as missing values, negative prices, and inconsistent formats.

3. **`Transform_Data`**:
   - Provides functions for calculating returns, volatility-adjusted metrics, and transforming data into analysis-ready formats.

4. **`Organize_Data`**:
   - Focuses on categorizing, grouping, and generating derived datasets for targeted analyses.

5. **`Extend_Data`**:
   - Advanced methods for merging datasets, adjusting for risk-free rates, and reconstructing bond prices using yield data.

### Initialization File

The `__init__.py` file consolidates key functions and classes for easy access, making it convenient to integrate the package into larger workflows.

```python
from Data.Transform_Data import *
from Data.Organize_Data import *
from Data.Get_Data import get_yahoo_finance_data, load_prices_from_csv
```
