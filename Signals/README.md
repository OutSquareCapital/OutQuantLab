
# Signals Library

## Overview

The **Signals** library is an advanced framework for creating and analyzing financial signals, designed with multi-threading and parallelization in mind. It is organized into logical classes based on market effects, making it modular and adaptable for various quantitative strategies.

## Design Objectives

1. **Parallelism**: Final normalized signals are explicitly structured to support multi-threading, enabling efficient processing of large datasets.
2. **Market Effect Categorization**: Signals are grouped into logical classes, each targeting a distinct market effect:
   - **Trend**: Captures directional market behavior over varying timeframes.
   - **Acceleration**: Measures the change in momentum to detect shifts in market dynamics.
   - **Return Distribution**: Explores statistical properties like skewness and kurtosis to analyze distributional effects.
   - **Mean Reversion**: Identifies overbought or oversold conditions to exploit reversion opportunities.
   - **Risk Premium**: Produces baseline signals for systematic biases or fixed premiums.
3. **Conditional Signals**: Every signal can be conditioned on a trend, allowing adaptive responses based on market state.
4. **Efficiency**: Designed to leverage modern computational tools for maximum performance:
   - Vectorization for speed.
   - Custom Numba implementations to replace pandas-based operations like skewness and kurtosis.
   - Memory management to minimize intermediate storage and facilitate garbage collection.
   - Bottleneck and NumPy for optimized rolling computations.

## Module Architecture

### Signals_Normalization
This foundational module provides tools for preparing and standardizing signals:
- **Ratio Normalization**: Scales ratios between arrays to standardized ranges.
- **Sign Normalization**: Simplifies signals to directional indicators (+1, -1, 0).
- **Rolling Median Normalization**: Robustly adjusts signals to mitigate outliers.
- **Rolling Scalar Normalization**: Dynamically scales signals relative to their rolling average magnitude.

### Signals_Raw
Implements the core raw calculations that feed into the normalized modules:
- **Trend Detection**: Rolling averages and medians for identifying directional behavior.
- **Acceleration Metrics**: Measures changes in trends over different timeframes.
- **Distribution Statistics**: Provides rolling computations for skewness and kurtosis, re-implemented in Numba for speed.
- **Volatility Measures**: Computes both directional and composite volatility, enabling nuanced market behavior analysis.

### Signals_Normalized
This module provides actionable signals derived from normalized inputs. It organizes signals into logical classes:

#### Trend
Detects market direction using methods like mean and median price ratios, or rate-of-change indicators.

#### Acceleration
Captures shifts in market momentum with MACD-style metrics and second-order changes in trends.

#### Return Distribution
Leverages statistical measures like skewness and kurtosis to understand the distributional dynamics of returns.

#### Mean Reversion
Identifies opportunities when markets deviate from their historical norms, relying on normalized reversion signals.

#### Risk Premium
Generates fixed or constant signals to model systematic biases or assumptions about return distributions.

### Logical Workflow
The workflow ensures modularity and clarity:
1. **Raw Calculation**: Signals start with basic computations (e.g., rolling averages, ratios).
2. **Normalization**: These raw signals are then normalized to enhance their robustness.
3. **Conditioning**: Signals can be conditioned on trends, allowing dynamic adaptation to market states.
4. **Integration**: Combine signals from different classes into composite indicators for strategy development.

## Performance Optimization

1. **Parallelism and Multi-Threading**
   - Signals are explicitly structured for multi-threading, with minimal dependencies between computations.
   - The library efficiently handles multi-asset and multi-signal processing in parallel.

2. **Custom Implementations**
   - Numba is used to re-implement complex rolling computations, such as skewness and kurtosis, avoiding pandas overhead.
   - Bottleneck handles simpler rolling operations (mean, median) with a focus on speed and memory usage.

3. **Memory Management**
   - Intermediate arrays are minimized using nested functions and in-place operations.
   - This reduces memory pressure and ensures better garbage collection, crucial for handling large datasets.

4. **Vectorization**
   - The library extensively relies on NumPy for vectorized operations, reducing the need for Python loops.
   - NumExpr accelerates non-rolling calculations when applicable.

## Example Usage

```python
from Signals.Signals_Normalized import Trend, Acceleration, ReturnDistribution

prices_array = ...  # 2D numpy array (float32)
returns_array = ...  # 2D numpy array (float32)

# Calculate trend signals
trend_signal = Trend.mean_price_ratio(prices_array, LenST=20, LenLT=60)

# Calculate acceleration signals
acceleration_signal = Acceleration.mean_rate_of_change_macd(returns_array, LenST=10, LenLT=50, MacdLength=15)

# Calculate skewness signals from the return distribution
skew_signal = ReturnDistribution.skewness(returns_array, LenSmooth=5, LenSkew=10)

# Combine signals, conditioned on the trend
final_signal = trend_signal + acceleration_signal * skew_signal
```

## Conclusion

The **Signals** library is a versatile and high-performance tool for financial signal analysis. By categorizing signals into logical classes and emphasizing parallelization, it addresses the demands of modern quantitative finance. Whether for backtesting or live trading, it provides the precision and speed required for sophisticated strategy development.
