
# Signals

**Signals** is a Python package designed to generate, normalize, and analyze trading signals for financial markets. Built with performance and modularity in mind, the package integrates raw and normalized signal construction methods to provide a complete framework for systematic trading.

## Design Goals

1. **Performance-Centric**:
   - Core computations rely on optimized NumPy, Numba, and Bottleneck functions for high-speed execution.
   - Implements vectorized operations and avoids overhead from higher-level abstractions like pandas.

2. **Signal Modularity**:
   - The package separates raw signal generation, normalization, and composite signal analysis into distinct components for clarity and extensibility.

3. **Optimization for Large Datasets**:
   - Algorithms are designed to handle large-scale multi-asset datasets, leveraging parallelism and efficient memory usage.

## Key Functionalities

### 1. Signal Construction
- **Trend and Momentum Signals**:
  - Includes mean, median, and central price ratios calculated over short- and long-term horizons.
  - Supports rate-of-change calculations to capture momentum dynamics.
- **Acceleration Metrics**:
  - Implements MACD-style signals with variations based on price and rate-of-change metrics.
- **Mean Reversion Indicators**:
  - Constructs signals that exploit short-term reversals and overextensions.

### 2. Normalization and Conditioning
- **Standard Normalization**:
  - Signals are standardized using ratio, sign, and relative normalization methods.
- **Rolling Metrics**:
  - Supports rolling median and standard deviation normalizations to smooth signal variability.
- **Trend-Conditioned Indicators**:
  - Combines signals with overarching trend indicators for adaptive strategies.

### 3. Composite Signal Framework
- **Seasonality and Breakout Analysis**:
  - Seasonal signals incorporate calendar-based patterns, such as day-of-week and quarter-of-year trends.
  - Breakout strategies use relative price movements against historical snapshots.
- **Risk Premium Signals**:
  - Includes static and dynamic risk premium biases for systematic portfolio adjustments.

## Optimization Highlights

1. **Separation of Raw and Normalized Signals**:
   - Raw signals are computed directly from price and return arrays using efficient mathematical operations.
   - Normalization functions are decoupled to allow flexible post-processing and tuning.

2. **Parallelization and Vectorization**:
   - Uses Numba and Bottleneck for rolling computations to ensure fast execution on high-dimensional arrays.
   - Numba’s `njit` decorators enable parallel processing where applicable.

3. **Custom Normalization Techniques**:
   - Includes unique methods like rolling scalar normalization and trend-based conditioning for robust signal generation.

4. **Compatibility with Systematic Strategies**:
   - The modular design allows integration into broader trading frameworks with minimal adaptation.

### Initialization File

The `__init__.py` file provides a unified interface for accessing the package's functionalities:

```python
from Signals.Signals_Normalized import *
```

The **Signals** package is built to serve as the backbone for creating advanced trading systems, enabling systematic exploration of signals across various market conditions.
