import numpy as np
from Files import NDArrayFloat, N_THREADS
import numbagg as nb
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Callable
from typing import Any

def bfill(array: NDArrayFloat) -> NDArrayFloat:
    return nb.bfill(array, axis=0) # type: ignore
    
def shift_array(returns_array: NDArrayFloat, step:int = 1) -> NDArrayFloat:
    shifted_array = np.empty_like(returns_array, dtype=np.float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array


def process_in_blocks_parallel(
    array: NDArrayFloat, 
    block_size: int, 
    func:Callable[..., NDArrayFloat], 
    *args: Any,
    **kwargs: Any
    ) -> NDArrayFloat:

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