from outquantlab.metrics import rolling_scalar_normalisation
from outquantlab.typing_conventions import DataFrameFloat, ArrayFloat, Float32
from numpy import empty
from outquantlab.indicators import BaseIndic
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from outquantlab.backtest.data_arrays import DataArrays
from outquantlab.config_classes import BacktestConfig, BacktestResults

def process_backtest(
    returns_df: DataFrameFloat,
    config: BacktestConfig,
) -> BacktestResults:
    processor: IndicatorsProcessor = IndicatorsProcessor(
        indics_params=config.indics_params,
        returns_df=returns_df,
        total_returns_streams=len(config.multi_index)
    )
    returns_df = DataFrameFloat(
        data=processor.process_strategies(),
        index=returns_df.dates,
        columns=config.multi_index,
    )
    config.backtest_results.aggregate_raw_returns(returns_df=returns_df)
    return config.backtest_results


class IndicatorsProcessor:
    def __init__(
        self,
        indics_params: list[BaseIndic],
        returns_df: DataFrameFloat,
        total_returns_streams: int,
    ) -> None:
        self.indics_params: list[BaseIndic] = indics_params
        self.data_arrays: DataArrays = DataArrays(pct_returns=returns_df.get_array())
        self.assets_nb: int = returns_df.shape[1]
        self.start_index: int = 0
        self.results: ArrayFloat =empty(
            shape=(returns_df.shape[0], total_returns_streams),
            dtype=Float32,
        )

    def fill_results_array(
        self,
        results_list: list[ArrayFloat],
        params_nb: int,
    ) -> None:
        for i in range(params_nb):
            end_index: int = self.start_index + self.assets_nb
            self.results[:, self.start_index : end_index] = results_list[i]
            self.start_index = end_index

    def process_strategies(
        self,
    ) -> ArrayFloat:
        threads_nb: int = cpu_count() or 8
        with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
            for indic in self.indics_params:
                try:
                    results_list: list[ArrayFloat] = self._process_params_parallel(
                        indic=indic,
                        global_executor=global_executor,
                    )

                    self.fill_results_array(
                        results_list=results_list,
                        params_nb=indic.params_nb,
                    )

                except Exception as e:
                    raise Exception(f"Error processing indicator {indic.name}: {e}")

        return self.results

    def _process_params_parallel(
        self,
        indic: BaseIndic,
        global_executor: ThreadPoolExecutor,
    ) -> list[ArrayFloat]:
        def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
            return self._process_param(indic=indic, param_tuple=param_tuple)

        return list(global_executor.map(process_single_param, indic.param_combos))

    def _process_param(
        self, indic: BaseIndic, param_tuple: tuple[int, ...]
    ) -> ArrayFloat:
        return (
            rolling_scalar_normalisation(
                raw_signal=indic.execute(self.data_arrays, *param_tuple)
            )
            * self.data_arrays.adjusted_returns
        )
