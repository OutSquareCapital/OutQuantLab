from joblib import Parallel, delayed
import numpy as np
from .Backtest_Initialization import initialize_data_array, initialize_signals_array
from collections.abc import Callable

def process_param(
    func: Callable, 
    data_array: np.ndarray, 
    volatility_adjusted_pct_returns_array: np.ndarray, 
    param: dict[str, int]
    ) -> np.ndarray:
    
    return func(data_array, **param) * volatility_adjusted_pct_returns_array

def process_indicator_parallel(
    func:Callable, 
    data_array:np.ndarray, 
    adjusted_returns_array:np.ndarray, 
    params:list[dict[str, int]]
    ):
    
    return Parallel(n_jobs=-1, 
                    backend='threading'
                    )(delayed(
                            process_param)(
                                        func, 
                                        data_array, 
                                        adjusted_returns_array, 
                                        param
                                        ) for param in params)

def calculate_strategy_returns(
                            signals_array: np.ndarray,
                            data_arrays: dict[str, np.ndarray],
                            indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]],
                            adjusted_returns_array: np.ndarray,
                            progress_callback: Callable
                            ) -> np.ndarray:

    signal_col_index = 0
    total_columns = signals_array.shape[1]
    total_steps = 70 - 10

    for func, array_type, params in indicators_and_params.values():

        data_array = data_arrays[array_type]

        results = process_indicator_parallel(func, data_array, adjusted_returns_array, params)
        
        results_stacked = np.hstack(results) # type: ignore
        num_cols = results_stacked.shape[1]
        signals_array[:, signal_col_index:signal_col_index + num_cols] = results_stacked

        signal_col_index += num_cols

        progress = 10 + int(total_steps * signal_col_index / total_columns)
        progress_callback(progress, f"Backtesting Strategies: {signal_col_index}/{total_columns}...")

    return signals_array


def transform_signals_into_returns(prices_array: np.ndarray, 
                                    log_returns_array: np.ndarray,
                                    volatility_adjusted_pct_returns_array: np.ndarray, 
                                    asset_names: list[str],
                                    indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]],
                                    progress_callback: Callable
                                    ) -> np.ndarray:
    
    data_arrays = initialize_data_array(prices_array,
                                        log_returns_array)

    signals_array = initialize_signals_array(
                                            prices_array, 
                                            indicators_and_params, 
                                            asset_names
                                            )

    return calculate_strategy_returns(
                                    signals_array,
                                    data_arrays,
                                    indicators_and_params,
                                    volatility_adjusted_pct_returns_array,
                                    progress_callback
                                    )