from Files import NDArrayFloat, IndicatorFunc
from concurrent.futures import ThreadPoolExecutor

def process_param(
    signals_instance,  
    func: IndicatorFunc, 
    adjusted_returns_array: NDArrayFloat, 
    param: dict[str, int]
    ) -> NDArrayFloat:
    # Plus besoin de getattr, on appelle directement la fonction stockée
    return func(signals_instance, **param) * adjusted_returns_array

def process_indicator_parallel(
    signals_instance,
    func: IndicatorFunc, 
    adjusted_returns_array: NDArrayFloat, 
    params: list[dict[str, int]],
    global_executor: ThreadPoolExecutor
) -> list[NDArrayFloat]:
    def process_single_param(param: dict[str, int]) -> NDArrayFloat:
        return process_param(signals_instance, func, adjusted_returns_array, param)

    results = list(global_executor.map(process_single_param, params))
    return results