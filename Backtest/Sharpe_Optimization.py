from Utilitary import ArrayFloat, Float32
import numpy as np
from Metrics import rolling_sharpe_ratios, shift_array

def broadcast_median(array: ArrayFloat) -> ArrayFloat:
    medians = np.nanmedian(array, axis=1)
    return np.tile(medians[:, np.newaxis], (1, array.shape[1]))

def relative_sharpe_on_confidence_period(
    returns_array: ArrayFloat,
    confidence_lookback: int = 2500
    ) -> ArrayFloat:

    def count_non_nan(x: ArrayFloat) -> ArrayFloat:
        return np.cumsum(~np.isnan(x), axis=0, dtype=Float32)

    sharpe_array: ArrayFloat = rolling_sharpe_ratios(
        returns_array=returns_array, 
        length = returns_array.shape[0], 
        min_length = 20
        )
    non_nan_counts: ArrayFloat = count_non_nan(sharpe_array)
    rolling_median_sharpe: ArrayFloat = broadcast_median(array=sharpe_array)
    normalized_sharpes: ArrayFloat = (
        sharpe_array - rolling_median_sharpe
        ) * (
            (non_nan_counts / confidence_lookback)**0.5
            ) + 1
        
    clipped_sharpes = np.clip(normalized_sharpes, 0, 2)
    return returns_array * shift_array(returns_array=clipped_sharpes)