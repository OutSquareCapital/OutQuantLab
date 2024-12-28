import numpy as np
import pandas as pd
from Database import N_THREADS
from Utilitary import ArrayFloat, ProgressFunc, DataFrameFloat, Float32
from concurrent.futures import ThreadPoolExecutor
from Config import Indicator
from Indicators import IndicatorsMethods
from Config import Indicator, ClustersTree

def generate_multi_index_process(
    indicators_params: list[Indicator], 
    asset_names: list[str], 
    assets_clusters: ClustersTree, 
    indics_clusters: ClustersTree
    ) -> pd.MultiIndex:

    asset_to_clusters = assets_clusters.map_nested_clusters_to_entities()

    indic_to_clusters = indics_clusters.map_nested_clusters_to_entities()

    multi_index_tuples: list[tuple[str, str, str, str, str, str, str]] = []

    for indic in indicators_params:
        for param in indic.param_combos:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                asset_cluster1, asset_cluster2 = asset_to_clusters[asset]
                indic_cluster1, indic_cluster2 = indic_to_clusters[indic.name]
                multi_index_tuples.append((
                    asset_cluster1, asset_cluster2, asset, 
                    indic_cluster1, indic_cluster2, 
                    indic.name, param_str
                ))

    return pd.MultiIndex.from_tuples( # type: ignore
        multi_index_tuples,
        names=["AssetCluster", "AssetSubCluster", "Asset", "IndicCluster", "IndicSubCluster", "Indicator", "Param"]
    )

def calculate_strategy_returns(
    pct_returns_array: ArrayFloat, 
    indicators_params: list[Indicator],
    indics_methods: IndicatorsMethods,
    dates_index: pd.DatetimeIndex,
    multi_index: pd.MultiIndex,
    progress_callback: ProgressFunc
    ) -> DataFrameFloat:
    signal_col_index = 0
    global_executor = ThreadPoolExecutor(max_workers=N_THREADS)
    indics_methods.process_data(pct_returns_array)
    total_returns_streams = int(multi_index.shape[0])
    signals_array: ArrayFloat = np.empty((pct_returns_array.shape[0], total_returns_streams), dtype=Float32)
    total_assets_count = pct_returns_array.shape[1]

    import time
    start = time.perf_counter()
    for indic in indicators_params:
        results = indics_methods.process_indicator_parallel(
            indic.func, 
            indic.param_combos, 
            global_executor
        )

        for result in results:
            signals_array[:, signal_col_index:signal_col_index + total_assets_count] = result
            signal_col_index += total_assets_count

        progress_callback(
            int(100 * signal_col_index / total_returns_streams),
            f"Backtesting Strategies: {signal_col_index}/{total_returns_streams}..."
        )
    end = time.perf_counter() - start
    print(f"Time taken: {end:.2f} seconds")
    return DataFrameFloat(
        data=signals_array,
        index=dates_index,
        columns=multi_index
        )