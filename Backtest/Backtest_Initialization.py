from typing import Tuple
from tqdm import tqdm
from Infrastructure import Fast_Tools as ft
import numpy as np

def create_progress_bar(total:int, description="Processing"):

    pbar = tqdm(total=total, desc=description)

    def update_progress():
        pbar.update(1)

    return pbar, update_progress

def initialize_returns_array(prices_array: np.ndarray,
                            log_returns_array: np.ndarray,
                            indicators_and_params: dict,
                            asset_names: list
                            ) -> Tuple[np.ndarray, dict, any, any, int, int, int, int]:
    
    total_days = prices_array.shape[0]

    num_assets = len(asset_names)
    num_params = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
    num_indicators = len(indicators_and_params)
    total_return_streams = num_assets * num_params

    signals_array = np.full((total_days, total_return_streams), np.nan, dtype=np.float32)

    shifted_log_returns = ft.shift_array(log_returns_array)
    shifted_prices = ft.shift_array(prices_array)
    data_arrays = {
        'returns_array': shifted_log_returns,
        'prices_array': shifted_prices
    }

    print(f'processing {num_params} params from {num_indicators} indicators on {num_assets} assets, for a total of {total_return_streams} individuals strategies...')

    return signals_array, data_arrays,  num_indicators