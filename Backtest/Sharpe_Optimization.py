from Utilitary import ArrayFloat, Float32
import numpy as np
from Metrics import rolling_sharpe_ratios, rolling_mean

def relative_sharpe_on_confidence_period(
    returns_array: ArrayFloat,
    sharpe_lookback:int, 
    confidence_lookback: int = 2500
    ) -> ArrayFloat:

    def count_non_nan(x: ArrayFloat) -> ArrayFloat:
        return np.cumsum(~np.isnan(x), axis=0, dtype=Float32)

    sharpe_array: ArrayFloat =rolling_sharpe_ratios(
        returns_array=returns_array, 
        length = sharpe_lookback, 
        min_length = 1
        )
    mean_sharpe_array: ArrayFloat = rolling_mean( array=sharpe_array, length=20, min_length=1)
    non_nan_counts: ArrayFloat = count_non_nan(mean_sharpe_array)
    rolling_median_sharpe = np.nanmedian(mean_sharpe_array, axis=1)
    
    normalized_sharpes: ArrayFloat = (
        mean_sharpe_array - rolling_median_sharpe[:, np.newaxis]
        ) * (
            (non_nan_counts / confidence_lookback)**0.5
            ) + 1
    return np.clip(normalized_sharpes, 0, None)