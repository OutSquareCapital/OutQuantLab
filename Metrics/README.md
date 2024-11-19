
# Metrics

**Metrics** is a Python package developed with the ultimate goal of eliminating the reliance on pandas or polars, transitioning entirely to optimized NumPy arrays, Numba, and Bottleneck. This approach ensures not only superior computational efficiency but also significantly reduced memory usage, particularly for parallelized operations on large datasets.

## Design Philosophy

1. **NumPy-Centric Optimization**:
   - All calculations are built on NumPy arrays for maximum performance and flexibility.
   - Operations are vectorized wherever possible to minimize Python overhead.

2. **Parallelization**:
   - Leveraging Numba's `prange` and optimized loops to parallelize computations across columns.
   - This approach scales seamlessly across multi-core architectures, far outperforming pandas or polars for rolling and aggregation tasks.

3. **Memory Efficiency**:
   - Designed to reduce memory overhead by avoiding unnecessary data copies.
   - Focuses on in-place operations and lightweight intermediate structures.

## Key Functionalities

### 1. Aggregation Metrics
- **Rolling Aggregations**:
  - Core metrics like mean, median, max, and min implemented with `bottleneck` and `numbagg` for high-speed rolling operations.
  - Weighted averages and quantile spreads efficiently handle edge cases with minimal computational overhead.

### 2. Distribution Metrics
- **Custom-Optimized Skewness and Kurtosis**:
  - Implemented using Numba to ensure both precision and speed.
  - Rolling calculations leverage incremental updates, avoiding redundant computations.

### 3. Volatility Metrics
- **Dynamic Volatility Models**:
  - Short-term and long-term volatility seamlessly blended using adjustable weights.
  - Composite volatility integrates multi-timeframe data while supporting annualization.

### 4. Performance Metrics
- **Risk-Adjusted Metrics**:
  - Efficient computation of Sharpe and Sortino ratios for rolling and expanding windows.
  - Uses conditional array logic to isolate downside risk in Sortino calculations.

### 5. Behavior Metrics
- **Autocorrelation Analysis**:
  - Rolling autocorrelation implemented with precise variance and covariance tracking.
  - Designed to uncover persistence and mean-reversion patterns in financial datasets.

## Why Transition Away From pandas and polars?

1. **Parallelization Efficiency**:
   - Pandas and polars rely heavily on single-threaded operations for many tasks.
   - NumPy and Numba provide far better scalability for parallelized array-based computations.

2. **Reduced Overhead**:
   - DataFrame structures introduce significant memory and computation overhead.
   - Arrays and optimized libraries like Bottleneck focus purely on numerical performance.

3. **Flexibility for Large Datasets**:
   - With Numba and Bottleneck, computations scale efficiently for very large arrays, something pandas struggles with in high-dimensional data.

## Optimization Highlights

- **Custom Algorithms**:
  - Incremental algorithms in Numba ensure rolling metrics like skewness and kurtosis are computed without reprocessing entire windows.
- **Minimal Memory Footprint**:
  - Designed to handle out-of-core data by focusing on array slicing and in-place transformations.
- **High-Performance Libraries**:
  - Integration with Bottleneck and Numbagg ensures industry-leading performance for rolling and aggregation functions.

### Initialization File

The `__init__.py` file consolidates all the package's functionality for streamlined integration:

```python
from .Aggregation import (rolling_mean, rolling_median, rolling_min, rolling_max, rolling_sum, rolling_weighted_mean, rolling_quantile_ratio)
from .Distribution import (rolling_skewness, rolling_kurtosis)
from .Volatility import (rolling_volatility, hv_composite_array, hv_composite_df, separate_volatility)
from .Performance import (rolling_sharpe_ratios_numpy, rolling_sharpe_ratios_df, rolling_sortino_ratios_numpy, expanding_sharpe_ratios_numpy)
from .Behavior import rolling_autocorrelation
```

The **Metrics** package is an ongoing effort to create a fully NumPy-driven library that maximizes computational power and efficiency while providing a robust suite of tools for financial analytics.
