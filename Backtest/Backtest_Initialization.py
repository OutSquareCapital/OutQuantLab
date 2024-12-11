from Infrastructure import Fast_Tools as ft
import numpy as np

def initialize_data_array(prices_array: np.ndarray,
                          log_returns_array: np.ndarray) -> dict[str, np.ndarray]:

    shifted_log_returns = ft.shift_array(log_returns_array)
    shifted_prices = ft.shift_array(prices_array)

    return {
        'returns_array': shifted_log_returns,
        'prices_array': shifted_prices
    }

def initialize_signals_array(
                            prices_array: np.ndarray,
                            indicators_and_params: dict,
                            asset_names: list,
                            ) -> np.ndarray:
    
    total_days = prices_array.shape[0]

    num_assets = len(asset_names)
    num_params = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
    total_return_streams = num_assets * num_params

    return np.full((total_days, total_return_streams), np.nan, dtype=np.float32)