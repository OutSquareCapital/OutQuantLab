import pandas as pd
import numpy as np
from Metrics import rolling_sharpe_ratios, rolling_mean
from Infrastructure import process_in_blocks_parallel
import numexpr as ne

def relative_sharpe_on_confidence_period(
    returns_df:pd.DataFrame, 
    sharpe_lookback:int, 
    confidence_lookback = 2500, 
    block_size = 500
    ) -> pd.DataFrame:

    sharpe_array = process_in_blocks_parallel(
        returns_df.values, 
        block_size=block_size,
        func=rolling_sharpe_ratios,
        length = sharpe_lookback,
        min_length = 125
    )

    mean_sharpe_array = process_in_blocks_parallel(
        sharpe_array, 
        block_size=block_size,
        func=rolling_mean,
        length=20, min_length=1
    )

    non_nan_counts = process_in_blocks_parallel(
        mean_sharpe_array, 
        block_size=block_size,
        func=lambda x: np.cumsum(~np.isnan(x), axis=0, dtype=np.float32)
    )

    rolling_median_sharpe = np.nanmedian(mean_sharpe_array, axis=1)[:, np.newaxis]

    normalized_sharpes = ne.evaluate(
        "(mean_sharpe_array - rolling_median_sharpe) * ((non_nan_counts / confidence_lookback)**0.5) + 1",
        local_dict={
            "mean_sharpe_array": mean_sharpe_array,
            "rolling_median_sharpe": rolling_median_sharpe,
            "non_nan_counts": non_nan_counts,
            "confidence_lookback": confidence_lookback
        }
    )


    clipped_sharpes = np.clip(normalized_sharpes, 0, None)

    return pd.DataFrame(
        clipped_sharpes, 
        index=returns_df.index, 
        columns= returns_df.columns,
        dtype=np.float32
        )