import pandas as pd
import numpy as np
from numpy.typing import NDArray
from Infrastructure import Fast_Tools as ft
from Files import PERCENTAGE_FACTOR
from collections.abc import Callable
from Infrastructure.Fast_Tools import shift_array
from Metrics import hv_composite
import yfinance as yf

def get_yahoo_finance_data(assets: list[str], file_path: str) -> None:

    data: pd.DataFrame|None = yf.download(
                            tickers=assets,
                            interval="1d",
                            auto_adjust=True,
                            progress=False,
                        )
    
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")

    data['Close'].to_parquet(
        file_path,
        index=True,
        engine="pyarrow"
    )

def load_prices(asset_names: list[str], file_path: str) -> pd.DataFrame:
    
    columns_to_load = ["Date"] + [name for name in asset_names]

    return pd.read_parquet(
        file_path,
        engine="pyarrow",
        columns=columns_to_load
    )

def calculate_volatility_adjusted_returns(
    pct_returns_array: NDArray[np.float32], 
    hv_array: NDArray[np.float32], 
    target_volatility: int = 15
    ) -> NDArray[np.float32]:

    vol_adj_position_size_shifted = shift_array(target_volatility / hv_array)

    return pct_returns_array * vol_adj_position_size_shifted

def calculate_equity_curves(returns_array: NDArray[np.float32]) -> NDArray[np.float32]:

    temp_array = returns_array.copy()

    mask = np.isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns = np.cumprod(1 + temp_array, axis=0)

    cumulative_returns[mask] = np.nan

    return cumulative_returns * PERCENTAGE_FACTOR

def log_returns_np(prices_array: NDArray[np.float32]) -> NDArray[np.float32]:

    if prices_array.ndim == 1:
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0] = np.nan
        log_returns_array[1:] = np.log(prices_array[1:] / prices_array[:-1])
    else:
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0, :] = np.nan
        log_returns_array[1:, :] = np.log(prices_array[1:] / prices_array[:-1])

    return log_returns_array

def generate_multi_index_process(
    indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]], 
    asset_names: list[str], 
    assets_clusters: dict[str, dict[str, list[str]]], 
    indics_clusters: dict[str, dict[str, list[str]]]
    ) -> pd.MultiIndex:

    asset_to_clusters = {
        asset: (cluster_level1, cluster_level2)
        for cluster_level1, subclusters in assets_clusters.items()
        for cluster_level2, assets in subclusters.items()
        for asset in assets
    }

    indic_to_clusters = {
        indic: (cluster_level1, cluster_level2)
        for cluster_level1, subclusters in indics_clusters.items()
        for cluster_level2, indics in subclusters.items()
        for indic in indics
    }

    multi_index_tuples = []

    for indicator_name, (_, _, params) in indicators_and_params.items():
        for param in params:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                asset_cluster1, asset_cluster2 = asset_to_clusters[asset]
                indic_cluster1, indic_cluster2 = indic_to_clusters[indicator_name]
                multi_index_tuples.append((
                    asset_cluster1, asset_cluster2, asset, 
                    indic_cluster1, indic_cluster2, 
                    indicator_name, param_str
                ))

    return pd.MultiIndex.from_tuples(
        multi_index_tuples,
        names=["AssetCluster", "AssetSubCluster", "Asset", "IndicCluster", "IndicSubCluster", "Indicator", "Param"]
    )


def process_data(
    data_prices_df: pd.DataFrame
    ) -> tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]:
    
    returns_df = data_prices_df.pct_change(fill_method=None)
    pct_returns_array = returns_df.to_numpy(dtype=np.float32)
    prices_array = ft.shift_array(calculate_equity_curves(pct_returns_array))
    log_returns_array = ft.shift_array(log_returns_np(prices_array))
    hv_array = hv_composite(pct_returns_array)
    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(
        pct_returns_array, 
        hv_array
    )

    return prices_array, log_returns_array, volatility_adjusted_pct_returns