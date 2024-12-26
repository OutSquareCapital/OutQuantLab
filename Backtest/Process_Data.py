import pandas as pd
import numpy as np
from numpy.typing import NDArray
from Files import PERCENTAGE_FACTOR
from Infrastructure import shift_array
from Metrics import hv_composite
import yfinance as yf # type: ignore
from Config import IndicatorParams, ClustersTree

def get_yahoo_finance_data(assets: list[str], file_path: str) -> None:

    data: pd.DataFrame|None = yf.download( # type: ignore
                            tickers=assets,
                            interval="1d",
                            auto_adjust=True,
                            progress=False,
                        )

    if isinstance(data, pd.DataFrame):
        data['Close'].to_parquet( # type: ignore
            file_path,
            index=True,
            engine="pyarrow"
        )
    else:
        raise ValueError("Yahoo Finance Data Not Available")


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

    vol_adj_position_size_shifted:NDArray[np.float32] = shift_array(target_volatility / hv_array)

    return pct_returns_array * vol_adj_position_size_shifted

def calculate_equity_curves(returns_array: NDArray[np.float32]) -> NDArray[np.float32]:

    temp_array:NDArray[np.float32] = returns_array.copy()

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
    indicators_and_params: list[IndicatorParams], 
    asset_names: list[str], 
    assets_clusters: ClustersTree, 
    indics_clusters: ClustersTree
    ) -> pd.MultiIndex:

    asset_to_clusters = assets_clusters.map_nested_clusters_to_assets()

    indic_to_clusters = indics_clusters.map_nested_clusters_to_assets()

    multi_index_tuples: list[tuple[str, str, str, str, str, str, str]] = []

    for indic in indicators_and_params:
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


def process_data(
    data_prices_df: pd.DataFrame
    ) -> tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]:
    
    returns_df = data_prices_df.pct_change(fill_method=None) # type: ignore
    pct_returns_array: NDArray[np.float32] = returns_df.to_numpy(dtype=np.float32) # type: ignore
    prices_array = shift_array(calculate_equity_curves(pct_returns_array))
    log_returns_array = shift_array(log_returns_np(prices_array))
    hv_array = hv_composite(pct_returns_array)
    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(
        pct_returns_array, 
        hv_array
    )

    return prices_array, log_returns_array, volatility_adjusted_pct_returns