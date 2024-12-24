import numpy as np
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

def process_param(
    func: Callable, 
    data_array: np.ndarray, 
    adjusted_returns_array: np.ndarray, 
    param: dict[str, int]
    ) -> np.ndarray:

    return func(data_array, **param) * adjusted_returns_array

def process_indicator_parallel(
    func: Callable, 
    data_array: np.ndarray, 
    adjusted_returns_array: np.ndarray, 
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