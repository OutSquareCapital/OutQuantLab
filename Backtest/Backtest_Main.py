import numpy as np
from numpy.typing import NDArray
import pandas as pd
from collections.abc import Callable
from Files import N_THREADS
from concurrent.futures import ThreadPoolExecutor
from .Process_Indicators import process_indicator_parallel
from .Process_Data import (
load_prices, 
generate_multi_index_process,
process_data
)
from dataclasses import dataclass
from Config import IndicatorParams

@dataclass(slots=True)
class BacktestData:
    prices_array: NDArray[np.float32]
    log_returns_array: NDArray[np.float32]
    adjusted_returns_array: NDArray[np.float32]
    signals_array: NDArray[np.float32]
    indicators_and_params: list[IndicatorParams]

@dataclass(slots=True)
class BacktestStructure:
    dates_index: pd.Index
    multi_index: pd.MultiIndex
    total_returns_streams: int
    total_assets_count: int

def calculate_strategy_returns(
    backtest_data: BacktestData,
    backtest_structure: BacktestStructure,
    progress_callback: Callable[[int, str], None]
) -> pd.DataFrame:
    signal_col_index = 0
    global_executor = ThreadPoolExecutor(max_workers=N_THREADS)

    for indic in backtest_data.indicators_and_params:

        data_array = backtest_data.prices_array if indic.array_type == 'prices_array' else backtest_data.log_returns_array
        results = process_indicator_parallel(indic.func, data_array, backtest_data.adjusted_returns_array, indic.param_combos, global_executor)

        for result in results:
            backtest_data.signals_array[:, signal_col_index:signal_col_index + backtest_structure.total_assets_count] = result
            signal_col_index += backtest_structure.total_assets_count

        progress_callback(
            int(100 * signal_col_index / backtest_structure.total_returns_streams),
            f"Backtesting Strategies: {signal_col_index}/{backtest_structure.total_returns_streams}..."
        )

    return pd.DataFrame(
        backtest_data.signals_array,
        index=backtest_structure.dates_index,
        columns=backtest_structure.multi_index,
        dtype=np.float32,
    )

def initialize_backtest_config(
    file_path: str,
    asset_names: list[str],
    indicators_and_params: list[IndicatorParams],
    asset_clusters: dict[str, dict[str, list[str]]],
    indics_clusters: dict[str, dict[str, list[str]]]
    ) -> tuple[BacktestData, BacktestStructure]:
    multi_index = generate_multi_index_process(indicators_and_params, asset_names, asset_clusters, indics_clusters)
    prices_df = load_prices(asset_names, file_path)
    dates_index = prices_df.index
    prices_array, log_returns_array, adjusted_returns_array = process_data(prices_df)
    total_returns_streams = multi_index.shape[0]
    total_assets_count = prices_array.shape[1]
    signals_array = np.empty((prices_array.shape[0], total_returns_streams), dtype=np.float32)

    price_data = BacktestData(prices_array, log_returns_array, adjusted_returns_array, signals_array, indicators_and_params)
    signal_config = BacktestStructure(dates_index, multi_index, total_returns_streams, total_assets_count)
    return price_data, signal_config