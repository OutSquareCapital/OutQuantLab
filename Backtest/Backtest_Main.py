import numpy as np
import pandas as pd
from Files import N_THREADS, NDArrayFloat, ProgressFunc
from concurrent.futures import ThreadPoolExecutor
from .Process_Data import (
load_prices, 
generate_multi_index_process,
)
from dataclasses import dataclass
from Config import IndicatorMethod, ClustersTree
from Indicators import IndicatorsMethods

@dataclass(slots=True)
class BacktestData:
    signals_array: NDArrayFloat
    indicators_and_params: list[IndicatorMethod]
    dates_index: pd.DatetimeIndex
    multi_index: pd.MultiIndex
    total_returns_streams: int
    total_assets_count: int

def calculate_strategy_returns(
    backtest_data: BacktestData,
    indics_methods: IndicatorsMethods,
    progress_callback: ProgressFunc
) -> pd.DataFrame:
    signal_col_index = 0
    global_executor = ThreadPoolExecutor(max_workers=N_THREADS)

    for indic in backtest_data.indicators_and_params:
        results = indics_methods.process_indicator_parallel(
            indic.func, 
            indic.param_combos, 
            global_executor
        )

        for result in results:
            backtest_data.signals_array[:, signal_col_index:signal_col_index + backtest_data.total_assets_count] = result
            signal_col_index += backtest_data.total_assets_count

        progress_callback(
            int(100 * signal_col_index / backtest_data.total_returns_streams),
            f"Backtesting Strategies: {signal_col_index}/{backtest_data.total_returns_streams}..."
        )

    return pd.DataFrame(
        data=backtest_data.signals_array,
        index=backtest_data.dates_index,
        columns=backtest_data.multi_index,
        dtype=np.float32,
    )

def initialize_backtest_config(
    file_path: str,
    asset_names: list[str],
    indicators_and_params: list[IndicatorMethod],
    asset_clusters: ClustersTree,
    indics_clusters: ClustersTree,
    indics_methods: IndicatorsMethods
    ) -> BacktestData:
    multi_index = generate_multi_index_process(indicators_and_params, asset_names, asset_clusters, indics_clusters)
    prices_df = load_prices(asset_names, file_path)
    dates_index: pd.DatetimeIndex = prices_df.index # type: ignore
    indics_methods.process_data(prices_df)
    total_returns_streams = int(multi_index.shape[0]) # type: ignore
    total_assets_count = indics_methods.prices_array.shape[1]
    signals_array = np.empty((indics_methods.prices_array.shape[0], total_returns_streams), dtype=np.float32)

    return BacktestData(signals_array, indicators_and_params, dates_index, multi_index, total_returns_streams, total_assets_count)