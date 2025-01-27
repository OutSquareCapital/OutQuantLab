from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

from numpy import empty

from outquantlab.config_classes import BacktestConfig
from outquantlab.indicators import BaseIndic, DataArrays
from outquantlab.typing_conventions import ArrayFloat, Float32


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


def process_strategies(
    data_arrays: DataArrays,
    backtest_config: BacktestConfig,
) -> ArrayFloat:
    signals_array: ArrayFloat = empty(
        shape=(
            data_arrays.prices_array.shape[0],
            backtest_config.total_returns_streams,
        ),
        dtype=Float32,
    )
    start_index: int = 0
    threads_nb: int = cpu_count() or 8
    with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
        for indic in backtest_config.indics_params:
            try:
                results: list[ArrayFloat] = process_indicator_parallel(
                    indic=indic,
                    data_arrays=data_arrays,
                    global_executor=global_executor,
                )

                for i in range(indic.strategies_nb):
                    end_index: int = start_index + backtest_config.assets_nb
                    signals_array[:, start_index:end_index] = results[i]
                    start_index = end_index

                backtest_config.progress.get_strategies_process_progress(
                    start_index=start_index,
                    total_returns_streams=backtest_config.total_returns_streams,
                )
            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return signals_array
