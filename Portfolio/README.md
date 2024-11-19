
# Portfolio

**Portfolio** is a Python package for constructing, analyzing, and optimizing financial portfolios. It combines static and dynamic clustering, performance evaluation, trading cost analysis, and weighting methods to provide a comprehensive toolkit for systematic portfolio management.

## Design Philosophy

1. **Hierarchy-Driven Analysis**:
   - Supports recursive portfolio structures, allowing for top-down or bottom-up asset aggregation.
   - Enables clustering assets into categories and subcategories dynamically or statically.

2. **Efficiency in Large Portfolios**:
   - Utilizes optimized libraries like NumPy, Bottleneck, and Numba for efficient computation.
   - Vectorized operations reduce processing time for high-dimensional datasets.

3. **Dynamic Adaptation**:
   - Incorporates dynamic clustering and weight adjustments based on asset availability and market conditions.

## Key Functionalities

### 1. Static and Dynamic Clustering
- **Static Clusters**:
  - Categorize assets into fixed hierarchies such as ratios, ensembles, and asset classes.
  - Generate recursive averages across these static structures for flexible portfolio analysis.
- **Dynamic Clusters**:
  - Cluster assets based on correlation or distance metrics, with support for multi-level clustering (e.g., subclusters and sub-subclusters).
  - Flatten unnecessary cluster hierarchies to simplify analysis.

### 2. Weight Generation and Normalization
- **Static Weights**:
  - Equal weighting within portfolio hierarchies, adjusted for multi-level structures.
- **Dynamic Weights**:
  - Adjust weights dynamically based on asset availability, ensuring fair allocation without volatility reduction.

### 3. Performance Evaluation
- **Risk-Adjusted Metrics**:
  - Calculate relative Sharpe ratios based on rolling and expanding confidence intervals.
- **Daily Averages**:
  - Generate daily average returns at the global level or grouped by asset class, method, or parameter.

### 4. Trading Cost Analysis
- **Cost Limits**:
  - Analyze the impact of trading costs on Sharpe ratios over varying timeframes.
- **Cost-Adjusted Returns**:
  - Adjust portfolio returns dynamically by accounting for transaction costs.

## Optimization Highlights

1. **Recursive Portfolio Structures**:
   - Supports recursive generation of means for portfolios and strategies, enabling multi-layered analysis.
   - Handles complex hierarchies without manual intervention.

2. **Vectorized and Parallelized Operations**:
   - Uses Bottleneck for rolling statistics and Numba for parallel computations.
   - Optimized for large-scale portfolio simulations with minimal memory overhead.

3. **Robust Trading Cost Adjustments**:
   - Incorporates adaptive cost thresholds to validate and adjust returns, ensuring realistic performance estimates.

### Initialization File

The `__init__.py` file integrates key functionalities for easy access:

```python
from Portfolio.Static_Clusters import calculate_daily_average_returns, generate_recursive_means, generate_recursive_strategy_means, classify_assets
```

The **Portfolio** package is designed for systematic traders and portfolio managers who require a robust, scalable toolkit for analyzing and optimizing complex portfolios.
