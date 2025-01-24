from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

from numpy import empty
from pandas import MultiIndex

from outquantlab.backtest.process_strategies import (
    calculate_portfolio_returns,
    process_indicator_parallel,
)
from outquantlab.config_classes import (
    Asset,
    AssetsClusters,
    IndicsClusters,
    generate_multi_index_process,
)
from outquantlab.indicators import BaseIndic, DataArrays, DataDfs
from outquantlab.metrics import calculate_overall_mean
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, Float32


class Backtester:
    def __init__(
        self,
        data_arrays: DataArrays,
        data_dfs: DataDfs,
        indics_params: list[BaseIndic],
        assets: list[Asset],
        indics_clusters: IndicsClusters,
        assets_clusters: AssetsClusters,
    ) -> None:
        self.indics_params: list[BaseIndic] = indics_params
        self.assets: list[Asset] = assets
        self.data_dfs: DataDfs = data_dfs
        self.data_arrays: DataArrays = data_arrays
        self.data_arrays.process_data(
            pct_returns_array=self.data_dfs.select_data(
                assets_names=[asset.name for asset in assets]
            )
        )
        self.observations_nb: int = self.data_arrays.prices_array.shape[0]
        self.assets_count: int = self.data_arrays.prices_array.shape[1]
        self.strategies_nb: int = sum(
            [len(indic.param_combos) for indic in self.indics_params]
        )
        self.threads_nb: int = cpu_count() or 8
        self.multi_index: MultiIndex = generate_multi_index_process(
            indic_param_tuples=indics_clusters.get_clusters_tuples(
                entities=self.indics_params
            ),
            asset_tuples=assets_clusters.get_clusters_tuples(entities=self.assets),
        )
        self.clusters_nb: int = len(self.multi_index.names) - 1
        self.total_returns_streams: int = self.assets_count * self.strategies_nb
        self.signal_col_index: int = 0
        self.signals_array: ArrayFloat = empty(
            shape=(self.observations_nb, self.total_returns_streams), dtype=Float32
        )
        self.process_strategies()
        self.aggregate_raw_returns()

    def progress_callback(self, progress: int, message: str) -> None:
        print(f"[{progress}%] {message}")

    def get_strategies_process_progress(self, indic: BaseIndic) -> None:
        self.progress_callback(
            int(100 * self.signal_col_index / self.total_returns_streams),
            f"Processing {indic.name}...",
        )

    def get_aggregation_progress(self, i: int, returns_df: DataFrameFloat) -> None:
        self.progress_callback(
            int(100 * (self.clusters_nb - i) / self.clusters_nb),
            f"Aggregating {' > '.join(self.multi_index.names[:i])}: {len(returns_df.columns)} columns left...",
        )

    def get_backtest_completion(self) -> None:
        self.progress_callback(100, "Backtest Completed!")

    def fill_signals_array(self, results: list[ArrayFloat]) -> None:
        results_len: int = len(results)
        for i in range(results_len):
            end_index: int = self.signal_col_index + self.assets_count
            self.signals_array[:, self.signal_col_index : end_index] = results[i]
            self.signal_col_index = end_index

    def get_returns_df(self) -> DataFrameFloat:
        returns_df = DataFrameFloat(
            data=self.signals_array,
            index=self.data_dfs.global_returns.dates,
            columns=self.multi_index,
        )
        del self.signals_array
        return returns_df

    def process_strategies(self) -> ArrayFloat:
        with ThreadPoolExecutor(max_workers=self.threads_nb) as global_executor:
            for indic in self.indics_params:
                try:
                    results: list[ArrayFloat] = process_indicator_parallel(
                        indic=indic,
                        global_executor=global_executor,
                    )

                    self.fill_signals_array(results=results)

                    self.get_strategies_process_progress(indic=indic)
                except Exception as e:
                    raise Exception(f"Error processing indicator {indic.name}: {e}")

        return self.signals_array

    def aggregate_raw_returns(self) -> None:
        raw_adjusted_returns_df = self.get_returns_df()

        for i in range(self.clusters_nb, 0, -1):
            raw_adjusted_returns_df: DataFrameFloat = calculate_portfolio_returns(
                returns_df=raw_adjusted_returns_df,
                grouping_levels=self.multi_index.names[:i],
            )
            if i == 5:
                raw_adjusted_returns_df.dropna(axis=0, how="any", inplace=True)  # type: ignore
                self.data_dfs.sub_portfolio_ovrll = DataFrameFloat(
                    data=raw_adjusted_returns_df
                )

            if i == 2:
                raw_adjusted_returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore
                self.data_dfs.sub_portfolio_roll = DataFrameFloat(
                    data=raw_adjusted_returns_df
                )

            self.get_aggregation_progress(i=i, returns_df=raw_adjusted_returns_df)

        self.get_backtest_completion()

        raw_adjusted_returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore

        self.data_dfs.global_returns = DataFrameFloat(
            data=calculate_overall_mean(
                array=raw_adjusted_returns_df.get_array(), axis=1
            ),
            index=raw_adjusted_returns_df.dates,
            columns=["Portfolio"],
        )
