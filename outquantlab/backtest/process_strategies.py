from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

from outquantlab.config_classes import BacktestConfig, BacktestResults
from outquantlab.indicators import BaseIndic, DataArrays
from outquantlab.typing_conventions import ArrayFloat


def process_strategies(
    data_arrays: DataArrays,
    backtest_config: BacktestConfig,
) -> ArrayFloat:
    backtest_results = BacktestResults(assets_nb=data_arrays.prices_array.shape[1])
    backtest_results.get_results_array(
        nb_days=data_arrays.prices_array.shape[0],
        total_returns_streams=len(backtest_config.multi_index),
    )
    threads_nb: int = cpu_count() or 8

    with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
        for indic in backtest_config.indics_params:
            try:
                results: list[ArrayFloat] = process_params_parallel(
                    indic=indic,
                    data_arrays=data_arrays,
                    global_executor=global_executor,
                )

                backtest_results.fill_results_array(
                    results=results, strategies_nb=indic.strategies_nb
                )

            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return backtest_results.results


def process_params_parallel(
    indic: BaseIndic,
    data_arrays: DataArrays,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(
            indic=indic, data_arrays=data_arrays, param_tuple=param_tuple
        )

    return list(global_executor.map(process_single_param, indic.param_combos))


def process_param(
    indic: BaseIndic, data_arrays: DataArrays, param_tuple: tuple[int, ...]
) -> ArrayFloat:
    return indic.execute(data_arrays, *param_tuple) * data_arrays.adjusted_returns_array
