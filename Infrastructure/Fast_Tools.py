import numpy as np
from numpy.typing import NDArray
import numbagg as nb
from concurrent.futures import ThreadPoolExecutor
from Files import N_THREADS

def bfill(array: NDArray[np.float32]) -> NDArray[np.float32]:
    return nb.bfill(array, axis=0)
    
def shift_array(returns_array: NDArray[np.float32], step:int = 1) -> NDArray[np.float32]:
    shifted_array = np.empty_like(returns_array, dtype=np.float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array


def process_in_blocks_parallel(array: NDArray[np.float32], block_size: int, func, *args, **kwargs) -> NDArray[np.float32]:

    num_cols: int = array.shape[1]
    num_blocks_to_process = max(int(num_cols/block_size), 1)
    max_threads = min(N_THREADS, num_blocks_to_process)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(
                func, array[:, start_col:min(start_col + block_size, num_cols)], *args, **kwargs
            )
            for start_col in range(0, num_cols, block_size)
        ]
        results = [future.result() for future in futures]

    return np.hstack(results)