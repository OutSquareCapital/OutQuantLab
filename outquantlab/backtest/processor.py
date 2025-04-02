from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

from numpy import empty

from outquantlab.core import BacktestConfig, BacktestResults
from outquantlab.indicators import BaseIndic, DataArrays, get_data_arrays
from outquantlab.structures import ArrayFloat, DataFrameFloat, Float32


def process_backtest(
    returns_df: DataFrameFloat,
    config: BacktestConfig,
) -> BacktestResults:
    processor: IndicatorsProcessor = IndicatorsProcessor(
        assets_nb=returns_df.shape[1],
        days_nb=returns_df.shape[0],
        total_returns_streams=len(config.multi_index),
    )
    returns_df = DataFrameFloat(
        data=processor.process_strategies(
            indics_params=config.indics_params,
            data_arrays=get_data_arrays(pct_returns=returns_df.get_array()),
        ),
        index=returns_df.dates,
        columns=config.multi_index,
    )
    aggregate_raw_returns(returns_df=returns_df, results=config.backtest_results)
    return config.backtest_results

def aggregate_raw_returns(returns_df: DataFrameFloat, results: BacktestResults) -> None:
    for lvl in range(results.clusters_depth, 0, -1):
        returns_df.get_portfolio_returns(grouping_levels=returns_df.columns.names[:lvl])
        returns_df.clean_nans()
        key_name: str = returns_df.columns.names[lvl - 1]
        results[key_name] = returns_df

class IndicatorsProcessor:
    def __init__(
        self,
        assets_nb: int,
        days_nb: int,
        total_returns_streams: int,
    ) -> None:
        self.assets_nb: int = assets_nb
        self.start_index: int = 0
        self.results: ArrayFloat = empty(
            shape=(days_nb, total_returns_streams),
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
        self, indics_params: list[BaseIndic], data_arrays: DataArrays
    ) -> ArrayFloat:
        threads_nb: int = cpu_count() or 8
        with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
            for indic in indics_params:
                try:
                    results_list: list[ArrayFloat] = indic.process_params_parallel(
                        data_arrays=data_arrays,
                        global_executor=global_executor,
                    )

                    self.fill_results_array(
                        results_list=results_list,
                        params_nb=indic.params.quantity,
                    )

                except Exception as e:
                    raise Exception(f"Error processing indicator {indic}: {e}")

        return self.results
