from Files import NDArrayFloat, IndicatorFunc
from concurrent.futures import ThreadPoolExecutor

def process_param(
    func: IndicatorFunc, 
    data_array: NDArrayFloat, 
    adjusted_returns_array: NDArrayFloat, 
    param: dict[str, int]
    ) -> NDArrayFloat:

    return func(data_array, **param) * adjusted_returns_array

def process_indicator_parallel(
    func: IndicatorFunc, 
    data_array: NDArrayFloat, 
    adjusted_returns_array: NDArrayFloat, 
    params: list[dict[str, int]],
    global_executor: ThreadPoolExecutor
) -> list[NDArrayFloat]:
    def process_single_param(param: dict[str, int]) -> NDArrayFloat:
        return process_param(func, data_array, adjusted_returns_array, param)

    results = list(global_executor.map(process_single_param, params))
    return results