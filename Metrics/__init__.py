from .Aggregation import (rolling_mean, 
                         rolling_median,
                         rolling_min,
                         rolling_max,
                         rolling_central,
                         rolling_sum,
                         rolling_weighted_mean,
                         rolling_quantile_ratio
                         )

from .Distribution import (rolling_kurtosis, 
                          rolling_skewness)

from .Volatility import (rolling_volatility, 
                        hv_composite_array, 
                        hv_composite_df,
                        separate_volatility)

from .Performance import (rolling_sharpe_ratios_numpy, 
                         rolling_sharpe_ratios_df, 
                         rolling_sortino_ratios_numpy, 
                         expanding_sharpe_ratios_numpy)

import numpy as np

dummy_array_2d = np.random.rand(100, 10).astype(np.float32)


rolling_mean(dummy_array_2d, 10)
rolling_sum(dummy_array_2d, 10)
rolling_volatility(dummy_array_2d, 10)

del dummy_array_2d