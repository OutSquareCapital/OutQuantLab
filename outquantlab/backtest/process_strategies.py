import numpy as np
import pandas as pd
import os
from typing import Final
from outquantlab.typing_conventions import ArrayFloat, ProgressFunc, DataFrameFloat, Float32
from concurrent.futures import ThreadPoolExecutor
from outquantlab.indicators import BaseIndicator, ReturnsData

N_THREADS: Final = os.cpu_count() or 8


def process_param(
    indic: BaseIndicator, param_tuple: tuple[int, ...]
) -> ArrayFloat:
    return (
        indic.execute(*param_tuple)
        * indic.returns_data.adjusted_returns_array
    )


def process_indicator_parallel(
    indic: BaseIndicator,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(indic=indic, param_tuple=param_tuple)

    return list(global_executor.map(process_single_param, indic.param_combos))


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
    returns_data: ReturnsData,
    indicators_params: list[BaseIndicator],
    multi_index: pd.MultiIndex,
    progress_callback: ProgressFunc,
) -> DataFrameFloat:
    signal_col_index = 0
    total_returns_streams: int = returns_data.total_assets_count * sum(
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
                    global_executor=global_executor,
                )

                signal_col_index: int = fill_signals_array(
                    signals_array=signals_array,
                    results=results,
                    total_assets_count=returns_data.total_assets_count,
                    start_index=signal_col_index,
                )

                progress_callback(
                    int(100 * signal_col_index / total_returns_streams),
                    f"Backtesting Strategies: {signal_col_index}/{total_returns_streams}...",
                )
            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return DataFrameFloat(data=signals_array, index=returns_data.date_index, columns=multi_index)
