from Utilitary import ArrayFloat, DataFrameFloat, Float32
import numpy as np
from Metrics import rolling_sharpe_ratios, rolling_mean
import numexpr as ne # type: ignore
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Callable
from typing import Any
from Database import N_THREADS

def process_in_blocks_parallel(
    array: ArrayFloat, 
    block_size: int, 
    func:Callable[..., ArrayFloat], 
    *args: Any,
    **kwargs: Any
    ) -> ArrayFloat:

    num_cols: int = array.shape[1]
    num_blocks_to_process = max(int(num_cols/block_size), 1)
    max_threads = min(N_THREADS, num_blocks_to_process)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(
                func, array[:, start_col:min(start_col + block_size, num_cols)], *args, **kwargs # type: ignore
            )
            for start_col in range(0, num_cols, block_size)
        ]
        results = [future.result() for future in futures]

    return np.hstack(results)

def relative_sharpe_on_confidence_period(
    returns_df: DataFrameFloat,
    sharpe_lookback:int, 
    confidence_lookback: int = 2500, 
    block_size: int = 500
    ) -> DataFrameFloat:

    def count_non_nan(x: ArrayFloat) -> ArrayFloat:
        return np.cumsum(~np.isnan(x), axis=0, dtype=Float32)


    sharpe_array = process_in_blocks_parallel(
        returns_df.nparray, 
        block_size=block_size,
        func=rolling_sharpe_ratios,
        length = sharpe_lookback,
        min_length = 125
    )

    mean_sharpe_array = process_in_blocks_parallel(
        sharpe_array, 
        block_size=block_size,
        func=rolling_mean,
        length=20, 
        min_length=1
    )

    non_nan_counts = process_in_blocks_parallel(
        mean_sharpe_array, 
        block_size=block_size,
        func=count_non_nan
    )

    rolling_median_sharpe = np.nanmedian(mean_sharpe_array, axis=1)[:, np.newaxis]

    normalized_sharpes: ArrayFloat = ne.evaluate( # type: ignore
        "(mean_sharpe_array - rolling_median_sharpe) * ((non_nan_counts / confidence_lookback)**0.5) + 1",
        local_dict={
            "mean_sharpe_array": mean_sharpe_array,
            "rolling_median_sharpe": rolling_median_sharpe,
            "non_nan_counts": non_nan_counts,
            "confidence_lookback": confidence_lookback
        }
    )


    clipped_sharpes = np.clip(normalized_sharpes, 0, None)

    return DataFrameFloat(
        data=clipped_sharpes, 
        index=returns_df.dates,
        columns= returns_df.columns
        )