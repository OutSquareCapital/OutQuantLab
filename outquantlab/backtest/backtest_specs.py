from concurrent.futures import ThreadPoolExecutor
from os import cpu_count

from pandas import MultiIndex

from outquantlab.backtest.process_strategies import (
    process_indicator_parallel,
    get_signals_array,
    calculate_portfolio_returns,
)
from outquantlab.backtest.progress_statut import ProgressStatus
from outquantlab.config_classes import (
    Asset,
    AssetsClusters,
    IndicsClusters,
    generate_multi_index_process,
)
from outquantlab.metrics import calculate_overall_mean
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat
from outquantlab.indicators import BaseIndic, DataArrays, DataDfs


class Backtester:
    def __init__(
        self,
        data_dfs: DataDfs,
        indics_params: list[BaseIndic],
        assets: list[Asset],
        indics_clusters: IndicsClusters,
        assets_clusters: AssetsClusters,
    ) -> None:
        self.signal_col_index: int = 0
        data_arrays = DataArrays(
            returns_array=data_dfs.select_data(
                assets_names=[asset.name for asset in assets]
            )
        )
        multi_index: MultiIndex = generate_multi_index_process(
            indic_param_tuples=indics_clusters.get_clusters_tuples(
                entities=indics_params
            ),
            asset_tuples=assets_clusters.get_clusters_tuples(entities=assets),
        )

        total_returns_streams: int = data_arrays.prices_array.shape[1] * sum(
            [indic.strategies_nb for indic in indics_params]
        )
        clusters_nb: int = len(multi_index.names) - 1
        clusters_names: list[str] = multi_index.names
        self.progress: ProgressStatus = ProgressStatus(
            total_returns_streams=total_returns_streams, clusters_nb=clusters_nb
        )
        self.signals_array: ArrayFloat = get_signals_array(
            total_returns_streams=total_returns_streams,
            observations_nb=data_arrays.prices_array.shape[0],
        )
        self.process_strategies(
            data_arrays=data_arrays,
            indics_params=indics_params,
            assets_count=data_arrays.prices_array.shape[1],
        )
        data_dfs.global_returns = DataFrameFloat(
            data=self.signals_array,
            index=data_dfs.global_returns.dates,
            columns=multi_index,
        )
        del self.signals_array
        self.aggregate_raw_returns(
            data_dfs=data_dfs, clusters_nb=clusters_nb, clusters_names=clusters_names
        )

    def fill_signals_array(
        self, results: list[ArrayFloat], strategies_nb: int, assets_count: int
    ) -> None:
        for i in range(strategies_nb):
            end_index: int = self.signal_col_index + assets_count
            self.signals_array[:, self.signal_col_index : end_index] = results[i]
            self.signal_col_index = end_index

    def process_strategies(
        self, data_arrays: DataArrays, indics_params: list[BaseIndic], assets_count: int
    ) -> ArrayFloat:
        threads_nb: int = cpu_count() or 8
        with ThreadPoolExecutor(max_workers=threads_nb) as global_executor:
            for indic in indics_params:
                try:
                    results: list[ArrayFloat] = process_indicator_parallel(
                        indic=indic,
                        data_arrays=data_arrays,
                        global_executor=global_executor,
                    )

                    self.fill_signals_array(
                        results=results,
                        strategies_nb=indic.strategies_nb,
                        assets_count=assets_count,
                    )

                    self.progress.get_strategies_process_progress(
                        signal_col_index=self.signal_col_index
                    )
                except Exception as e:
                    raise Exception(f"Error processing indicator {indic.name}: {e}")

        return self.signals_array

    def aggregate_raw_returns(
        self, clusters_nb: int, clusters_names: list[str], data_dfs: DataDfs
    ) -> None:
        for i in range(clusters_nb, 0, -1):
            data_dfs.global_returns = calculate_portfolio_returns(
                returns_df=data_dfs.global_returns, grouping_levels=clusters_names[:i]
            )
            if i == 5:
                data_dfs.global_returns.dropna(axis=0, how="any", inplace=True)  # type: ignore
                data_dfs.sub_portfolio_ovrll = DataFrameFloat(
                    data=data_dfs.global_returns
                )

            if i == 2:
                data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore
                data_dfs.sub_portfolio_roll = DataFrameFloat(
                    data=data_dfs.global_returns
                )

            self.progress.get_aggregation_progress(i=i)

        data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore

        data_dfs.global_returns = DataFrameFloat(
            data=calculate_overall_mean(
                array=data_dfs.global_returns.get_array(), axis=1
            ),
            index=data_dfs.global_returns.dates,
            columns=["Portfolio"],
        )
