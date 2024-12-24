import numpy as np
import pandas as pd
from collections.abc import Callable
from Files import N_THREADS
from concurrent.futures import ThreadPoolExecutor
from .Process_Indicators import process_indicator_parallel, handle_progress
from .Process_Data import (
load_prices, 
generate_multi_index_process,
process_data
)

class BacktestProcess:
    def __init__(
        self,
        file_path: str,
        asset_names: list[str],
        asset_clusters: dict[str, dict[str, list[str]]],
        indics_clusters: dict[str, dict[str, list[str]]],
        indicators_and_params
        ):
        
        self.indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]]
        self.dates_index: pd.Index
        self.adjusted_returns_array: np.ndarray
        self.prices_array: np.ndarray
        self.log_returns_array: np.ndarray
        self.signals_array: np.ndarray
        self.total_assets_count: int
        self.total_returns_streams: int
        self.multi_index: pd.MultiIndex
        self.initialize_backtest_data(file_path, asset_names, indicators_and_params, asset_clusters, indics_clusters)
        
    def initialize_backtest_data(
        self, file_path: str, 
        asset_names: list[str], 
        indicators_and_params, 
        asset_clusters: dict[str, dict[str, list[str]]], 
        indics_clusters: dict[str, dict[str, list[str]]]):
        
        self.indicators_and_params = indicators_and_params
        self.multi_index = generate_multi_index_process(indicators_and_params, asset_names, asset_clusters, indics_clusters)
        prices_df = load_prices(asset_names, file_path)
        self.dates_index = prices_df.index
        self.prices_array, self.log_returns_array, self.adjusted_returns_array = process_data(prices_df)
        self.total_assets_count = self.prices_array.shape[1]
        self.total_returns_streams = self.multi_index.shape[0]
        self.signals_array = np.empty((self.prices_array.shape[0], self.total_returns_streams), dtype=np.float32)

    def calculate_strategy_returns(
        self,
        progress_callback: Callable = handle_progress
        ) -> pd.DataFrame:

        signal_col_index = int(0)
        global_executor = ThreadPoolExecutor(max_workers=N_THREADS)
        
        for func, array_type, params in self.indicators_and_params.values():

            data_array = self.prices_array if array_type == 'prices_array' else self.log_returns_array
            results = process_indicator_parallel(func, data_array, self.adjusted_returns_array, params, global_executor)

            for result in results:
                self.signals_array[:, signal_col_index:signal_col_index + self.total_assets_count] = result
                signal_col_index += self.total_assets_count

            progress = int(100 * signal_col_index / self.total_returns_streams)
            message = f"Backtesting Strategies: {signal_col_index}/{self.total_returns_streams}..."
            progress_callback(progress, message)

        return pd.DataFrame(
        self.signals_array, 
        index=self.dates_index, 
        columns=self.multi_index, 
        dtype=np.float32
        )