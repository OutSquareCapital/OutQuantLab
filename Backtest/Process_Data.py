import pandas as pd
import yfinance as yf # type: ignore
from Config import IndicatorMethod, ClustersTree

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

def generate_multi_index_process(
    indicators_and_params: list[IndicatorMethod], 
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