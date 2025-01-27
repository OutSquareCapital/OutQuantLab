from outquantlab.backtest.aggregate_returns import aggregate_raw_returns
from outquantlab.backtest.process_strategies import (
    get_signals_array,
    process_strategies,
)
from outquantlab.config_classes import ProgressStatus
from outquantlab.config_classes import (
    Asset,
    ConfigState,
    ClustersIndex,
)
from outquantlab.indicators import BaseIndic, DataArrays, DataDfs
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def execute_backtest(
    data_dfs: DataDfs,
    config: ConfigState
) -> None:
    indics_params: list[BaseIndic]=config.indics_collection.get_indics_params()
    assets: list[Asset]=config.assets_collection.get_all_active_entities()
    
    clusters_index: ClustersIndex = config.generate_multi_index_process(
        indics_params=indics_params,
        assets=assets
    )

    progress: ProgressStatus = clusters_index.get_progress()

    get_backtest_returns(
        data_dfs=data_dfs,
        indics_params=indics_params,
        clusters_index=clusters_index,
        progress=progress,
    )
    aggregate_raw_returns(
        data_dfs=data_dfs,
        clusters_nb=clusters_index.clusters_nb,
        clusters_names=clusters_index.clusters_names,
        progress=progress,
    )


def get_backtest_returns(
    data_dfs: DataDfs,
    indics_params: list[BaseIndic],
    clusters_index: ClustersIndex,
    progress: ProgressStatus,
) -> None:
    data_arrays: DataArrays = data_dfs.select_data()
    signals_array: ArrayFloat = get_signals_array(
        total_returns_streams=clusters_index.total_returns_streams,
        observations_nb=data_arrays.prices_array.shape[0],
    )
    signals_array = process_strategies(
        signals_array=signals_array,
        data_arrays=data_arrays,
        indics_params=indics_params,
        assets_count=clusters_index.assets_nb,
        progress=progress,
    )
    data_dfs.global_returns = DataFrameFloat(
        data=signals_array,
        index=data_dfs.global_returns.dates,
        columns=clusters_index.multi_index,
    )
