from pandas import MultiIndex

from outquantlab.backtest.process_strategies import (
    process_strategies,
    get_signals_array,
)
from outquantlab.backtest.aggregate_returns import aggregate_raw_returns
from outquantlab.backtest.progress_statut import ProgressStatus
from outquantlab.config_classes import (
    Asset,
    AssetsClusters,
    IndicsClusters,
    generate_multi_index_process,
)
from outquantlab.indicators import BaseIndic, DataArrays, DataDfs
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def execute_backtest(
    data_dfs: DataDfs,
    indics_params: list[BaseIndic],
    assets: list[Asset],
    indics_clusters: IndicsClusters,
    assets_clusters: AssetsClusters,
) -> None:
    data_arrays: DataArrays = data_dfs.select_data(
        assets_names=[asset.name for asset in assets]
    )
    multi_index: MultiIndex = generate_multi_index_process(
        indic_param_tuples=indics_clusters.get_clusters_tuples(entities=indics_params),
        asset_tuples=assets_clusters.get_clusters_tuples(entities=assets),
    )

    main_process_strategies(
        data_arrays=data_arrays,
        data_dfs=data_dfs,
        indics_params=indics_params,
        multi_index=multi_index,
    )


def main_process_strategies(
    data_arrays: DataArrays,
    data_dfs: DataDfs,
    indics_params: list[BaseIndic],
    multi_index: MultiIndex,
) -> None:
    total_returns_streams: int = len(multi_index)
    clusters_nb: int = len(multi_index.names) - 1
    clusters_names: list[str] = multi_index.names
    progress: ProgressStatus = ProgressStatus(
        total_returns_streams=total_returns_streams, clusters_nb=clusters_nb
    )

    signals_array: ArrayFloat = get_signals_array(
        total_returns_streams=total_returns_streams,
        observations_nb=data_arrays.prices_array.shape[0],
    )
    signals_array = process_strategies(
        signals_array=signals_array,
        data_arrays=data_arrays,
        indics_params=indics_params,
        assets_count=data_arrays.prices_array.shape[1],
        progress=progress,
    )
    data_dfs.global_returns = DataFrameFloat(
        data=signals_array,
        index=data_dfs.global_returns.dates,
        columns=multi_index,
    )
    del signals_array
    aggregate_raw_returns(
        data_dfs=data_dfs,
        clusters_nb=clusters_nb,
        clusters_names=clusters_names,
        progress=progress,
    )
