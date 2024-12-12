import numpy as np
from joblib import Parallel, delayed
import numbagg as nb

def bfill(array: np.ndarray) -> np.ndarray:
    return nb.bfill(array, axis=0)
    
def shift_array(returns_array: np.ndarray, step:int = 1) -> np.ndarray:
    shifted_array = np.empty_like(returns_array, dtype=np.float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array

def snapshot_at_intervals(prices_array: np.ndarray, snapshot_interval: int) -> np.ndarray:

    snapshot_indices = np.arange(0, prices_array.shape[0], snapshot_interval)

    snapshots = prices_array[snapshot_indices]

    repeated_snapshots = np.repeat(snapshots, snapshot_interval, axis=0)

    repeated_snapshots = repeated_snapshots[:prices_array.shape[0]]

    return repeated_snapshots

def process_in_blocks_parallel(array, block_size, func, *args, **kwargs):

    num_cols = array.shape[1]

    results = Parallel(n_jobs=-1, backend='threading')(
        delayed(func)(array[:, start_col:min(start_col + block_size, num_cols)], *args, **kwargs)
        for start_col in range(0, num_cols, block_size)
    )
    if results is list:
        return np.hstack(results)
