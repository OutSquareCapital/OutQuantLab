import numpy as np
from numpy.typing import NDArray
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

def process_param(
    func: Callable, 
    data_array: NDArray[np.float32], 
    adjusted_returns_array: NDArray[np.float32], 
    param: dict[str, int]
    ) -> NDArray[np.float32]:

    return func(data_array, **param) * adjusted_returns_array

def process_indicator_parallel(
    func: Callable, 
    data_array: NDArray[np.float32], 
    adjusted_returns_array: NDArray[np.float32], 
    params: list[dict[str, int]],
    global_executor: ThreadPoolExecutor
) -> list[np.ndarray]:
    results = list(
        global_executor.map(
            lambda param: process_param(func, data_array, adjusted_returns_array, param),
            params
        )
    )
    return results