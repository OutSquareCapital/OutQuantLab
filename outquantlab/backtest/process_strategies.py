from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from numpy import empty

from outquantlab.indicators import BaseIndic, DataArrays
from outquantlab.typing_conventions import ArrayFloat, Float32
from outquantlab.config_classes import ProgressStatus


def get_signals_array(observations_nb: int, total_returns_streams: int) -> ArrayFloat:
    return empty(
        shape=(observations_nb, total_returns_streams),
        dtype=Float32,
    )


def process_param(
    indic: BaseIndic, data_arrays: DataArrays, param_tuple: tuple[int, ...]
) -> ArrayFloat:
    return indic.execute(data_arrays, *param_tuple) * data_arrays.adjusted_returns_array


def process_indicator_parallel(
    indic: BaseIndic,
    data_arrays: DataArrays,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(
            indic=indic, data_arrays=data_arrays, param_tuple=param_tuple
        )

    return list(global_executor.map(process_single_param, indic.param_combos))


def fill_signals_array(
    signal_col_index: int,
    signals_array: ArrayFloat,
    results: list[ArrayFloat],
    strategies_nb: int,
    assets_count: int,
) -> int:
    for i in range(strategies_nb):
        end_index: int = signal_col_index + assets_count
        signals_array[:, signal_col_index:end_index] = results[i]
        signal_col_index = end_index

    return signal_col_index


def process_strategies(
    signals_array: ArrayFloat,
    data_arrays: DataArrays,
    indics_params: list[BaseIndic],
    assets_count: int,
    progress: ProgressStatus,
) -> ArrayFloat:
    threads_nb: int = cpu_count() or 8
    signal_col_index: int = 0
    with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
        for indic in indics_params:
            try:
                results: list[ArrayFloat] = process_indicator_parallel(
                    indic=indic,
                    data_arrays=data_arrays,
                    global_executor=global_executor,
                )

                signal_col_index = fill_signals_array(
                    signal_col_index=signal_col_index,
                    signals_array=signals_array,
                    results=results,
                    strategies_nb=indic.strategies_nb,
                    assets_count=assets_count,
                )

                progress.get_strategies_process_progress(
                    signal_col_index=signal_col_index
                )
            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return signals_array
