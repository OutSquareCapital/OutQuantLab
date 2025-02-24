from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from dataclasses import dataclass, field
from outquantlab.config_classes import BacktestConfig
from outquantlab.indicators import BaseIndic
from outquantlab.typing_conventions import ArrayFloat, Float32
from outquantlab.backtest.data_arrays import DataArrays
from numpy import empty

@dataclass(slots=True)
class BacktestResults:
    assets_nb: int
    start_index: int = 0
    results: ArrayFloat = field(default_factory=lambda: empty(shape=(0, 0), dtype=Float32))

    def get_results_array(self, nb_days: int, total_returns_streams: int) -> None:
        self.results = empty(
            shape=(nb_days, total_returns_streams),
            dtype=Float32,
        )

    def fill_results_array(
        self,
        results: list[ArrayFloat],
        strategies_nb: int,
    ) -> None:
        for i in range(strategies_nb):
            end_index: int = self.start_index + self.assets_nb
            self.results[:, self.start_index : end_index] = results[i]
            self.start_index = end_index


def process_strategies(
    data_arrays: DataArrays,
    backtest_config: BacktestConfig,
) -> ArrayFloat:
    backtest_results: BacktestResults = prepare_backtest_results(
        data_arrays=data_arrays,
        backtest_config=backtest_config,
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

def prepare_backtest_results(
    data_arrays: DataArrays,
    backtest_config: BacktestConfig,
) -> BacktestResults:
    backtest_results = BacktestResults(assets_nb=data_arrays.prices.shape[1])
    backtest_results.get_results_array(
        nb_days=data_arrays.prices.shape[0],
        total_returns_streams=len(backtest_config.multi_index),
    )
    return backtest_results

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
    return indic.execute(data_arrays, *param_tuple) * data_arrays.adjusted_returns
