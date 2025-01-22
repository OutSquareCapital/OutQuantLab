import numpy as np
import pandas as pd
import os
from typing import Final
from TypingConventions import ArrayFloat, ProgressFunc, DataFrameFloat, Float32
from concurrent.futures import ThreadPoolExecutor
from Indicators import BaseIndicator, ReturnsData, process_data

N_THREADS: Final = os.cpu_count() or 8


def process_param(
    indic: BaseIndicator, returns_data: ReturnsData, param: tuple[int, ...]
) -> ArrayFloat:
    return (
        indic.execute(returns_data=returns_data, *param)
        * returns_data.adjusted_returns_array
    )


def process_indicator_parallel(
    indic: BaseIndicator,
    params: list[tuple[int, ...]],
    returns_data: ReturnsData,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(indic=indic, returns_data=returns_data, param=param_tuple)

    return list(global_executor.map(process_single_param, params))


def fill_signals_array(
    signals_array: ArrayFloat,
    results: list[ArrayFloat],
    start_index: int,
    total_assets_count: int,
) -> int:
    results_len: int = len(results)
    for i in range(results_len):
        end_index: int = start_index + total_assets_count
        signals_array[:, start_index:end_index] = results[i]
        start_index = end_index

    return start_index


def calculate_strategy_returns(
    pct_returns_array: ArrayFloat,
    indicators_params: list[BaseIndicator],
    dates_index: pd.DatetimeIndex,
    multi_index: pd.MultiIndex,
    progress_callback: ProgressFunc,
) -> DataFrameFloat:
    returns_data: ReturnsData = process_data(pct_returns_array=pct_returns_array)
    signal_col_index = 0
    total_assets_count: int = returns_data.prices_array.shape[1]
    total_returns_streams: int = total_assets_count * sum(
        [indic.strategies_nb for indic in indicators_params]
    )
    signals_array: ArrayFloat = np.empty(
        shape=(returns_data.prices_array.shape[0], total_returns_streams), dtype=Float32
    )

    with ThreadPoolExecutor(max_workers=N_THREADS) as global_executor:
        for indic in indicators_params:
            try:
                results: list[ArrayFloat] = process_indicator_parallel(
                    indic=indic,
                    params=indic.param_combos,
                    returns_data=returns_data,
                    global_executor=global_executor,
                )

                signal_col_index: int = fill_signals_array(
                    signals_array=signals_array,
                    results=results,
                    total_assets_count=total_assets_count,
                    start_index=signal_col_index,
                )

                progress_callback(
                    int(100 * signal_col_index / total_returns_streams),
                    f"Backtesting Strategies: {signal_col_index}/{total_returns_streams}...",
                )
            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return DataFrameFloat(data=signals_array, index=dates_index, columns=multi_index)
