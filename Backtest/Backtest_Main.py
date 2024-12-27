import numpy as np
import pandas as pd
from Files import N_THREADS, NDArrayFloat, ProgressFunc
from concurrent.futures import ThreadPoolExecutor
from Config import Indicator
from Indicators import IndicatorsMethods

def calculate_strategy_returns(
    pct_returns_array: NDArrayFloat, 
    indicators_params: list[Indicator],
    indics_methods: IndicatorsMethods,
    dates_index: pd.Index,
    multi_index: pd.MultiIndex,
    progress_callback: ProgressFunc
    ) -> pd.DataFrame:
    signal_col_index = 0
    global_executor = ThreadPoolExecutor(max_workers=N_THREADS)
    indics_methods.process_data(pct_returns_array)
    total_returns_streams = int(multi_index.shape[0])
    signals_array = np.zeros((pct_returns_array.shape[0], total_returns_streams), dtype=np.float32)
    total_assets_count = pct_returns_array.shape[1]

    import time
    start = time.perf_counter()
    for indic in indicators_params:
        results = indics_methods.process_indicator_parallel(
            indic.func, 
            indic.param_combos, 
            global_executor
        )

        for result in results:
            signals_array[:, signal_col_index:signal_col_index + total_assets_count] = result
            signal_col_index += total_assets_count

        progress_callback(
            int(100 * signal_col_index / total_returns_streams),
            f"Backtesting Strategies: {signal_col_index}/{total_returns_streams}..."
        )
    end = time.perf_counter() - start
    print(f"Time taken: {end:.2f} seconds")

    return pd.DataFrame(
        data=signals_array,
        index=dates_index,
        columns=multi_index,
        dtype=np.float32
        )