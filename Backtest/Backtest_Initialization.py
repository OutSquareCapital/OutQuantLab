from typing import Tuple
from Infrastructure import Fast_Tools as ft
import numpy as np

def initialize_backtest(indicators_and_params: dict,
                        asset_names: list,
                        prices_array: np.ndarray)-> Tuple[int, int]:

    total_days = prices_array.shape[0]

    num_assets = len(asset_names)
    num_params = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
    num_indicators = len(indicators_and_params)
    total_return_streams = num_assets * num_params
    print(f'processing {num_params} params from {num_indicators} indicators on {num_assets} assets, for a total of {total_return_streams} individuals strategies...')
    
    return total_days, total_return_streams

def initialize_returns_array(prices_array: np.ndarray,
                            log_returns_array: np.ndarray,
                            total_days: int, 
                            total_return_streams: int
                            ) -> Tuple[np.ndarray, dict]:
    
    signals_array = np.full((total_days, total_return_streams), np.nan, dtype=np.float32)

    shifted_log_returns = ft.shift_array(log_returns_array)
    shifted_prices = ft.shift_array(prices_array)
    data_arrays = {
        'returns_array': shifted_log_returns,
        'prices_array': shifted_prices
    }

    return signals_array, data_arrays