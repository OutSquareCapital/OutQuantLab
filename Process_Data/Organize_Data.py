import numpy as np
import pandas as pd
from collections.abc import Callable
from Infrastructure import Fast_Tools as ft
from .Transform_Data import (
load_prices, 
generate_multi_index_process,
initialize_signals_array, 
process_data, 
get_total_return_streams_nb
)

class BacktestConfig:
    def __init__(
        self,
        file_path: str,
        asset_names: list[str], 
        indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]]):
        
        self.file_path = file_path
        self.asset_names = asset_names
        self.indicators_and_params = indicators_and_params
        self.dates_index: pd.Index
        self.volatility_adjusted_pct_returns: np.ndarray
        self.data_array: tuple[np.ndarray, np.ndarray]
        self.signals_array: np.ndarray
        self.multi_index: pd.MultiIndex = generate_multi_index_process(indicators_and_params, asset_names)
        self.initialize_backtest_data()
        
    def initialize_backtest_data(self):
        
        prices_df = load_prices(self.asset_names, self.file_path)
        self.dates_index = prices_df.index
        prices_array, log_returns_array, self.volatility_adjusted_pct_returns = process_data(prices_df)
        self.data_array = ft.shift_array(prices_array), ft.shift_array(log_returns_array)
        total_return_streams: int = get_total_return_streams_nb(self.indicators_and_params, self.asset_names)
        self.signals_array = initialize_signals_array(prices_array, total_return_streams)
