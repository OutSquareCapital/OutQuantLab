from ConfigClasses import (
    AssetsCollection,
    ClustersTree,
    IndicatorsCollection,
)
from DataBase import DataQueries
from TypingConventions import ArrayFloat, DataFrameFloat
import pandas as pd
from Metrics import pct_returns_np
import yfinance as yf  # type: ignore


class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def get_assets_returns(self, asset_names: list[str]) -> ArrayFloat:
        returns_df = DataFrameFloat(
            data=self.dbq.select(file="returns_data").load(names=asset_names)
        )
        return returns_df.nparray

    def get_initial_data(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=self.dbq.select(file="returns_data").load(names=["Date", "SPY"])
        )

    def refresh_yf_data(self, assets: list[str]) -> None:
        data: pd.DataFrame | None = yf.download(  # type: ignore
            tickers=assets,
            interval="1d",
            auto_adjust=True,
            progress=False,
        )
        if data is None:
            raise ValueError("Yahoo Finance Data Not Available")
        else:
            prices_data = DataFrameFloat(data=data["Close"])  # type: ignore

            returns_data = DataFrameFloat(
                data=pct_returns_np(prices_array=prices_data.nparray),
                columns=prices_data.columns,
                index=prices_data.dates,
            )
            
            assets_names: list[str] = prices_data.columns.to_list()

            self.dbq.select(file="price_data").save(data=prices_data)
            self.dbq.select(file="returns_data").save(data=returns_data)
            self.dbq.select(file="assets_names").save(data=assets_names)

    def get_assets_collection(self) -> AssetsCollection:
        return AssetsCollection(
            assets_to_test=self.dbq.select(file="assets_to_test").load(),
            asset_names=self.dbq.select(file="assets_names").load(),
        )

    def get_indicators_collection(self) -> IndicatorsCollection:
        return IndicatorsCollection(
            indicators_to_test=self.dbq.select(file="indics_to_test").load(),
            params_config=self.dbq.select(file="indics_params").load(),
        )

    def get_clusters_tree(self, cluster_type: str) -> ClustersTree:
        prefix = "Asset" if cluster_type == "assets" else "Indic"
        return ClustersTree(
            clusters=self.dbq.select(file=f"{cluster_type}_clusters").load(),
            prefix=prefix,
        )

    def save_assets_collection(self, assets_collection: AssetsCollection) -> None:
        self.dbq.select("assets_to_test").save(
            data=assets_collection.all_active_entities_dict
        )

    def save_indicators_collection(
        self, indics_collection: IndicatorsCollection
    ) -> None:
        self.dbq.select(file="indics_to_test").save(
            data=indics_collection.all_active_entities_dict
        )
        self.dbq.select(file="indics_params").save(
            data=indics_collection.all_params_config
        )

    def save_clusters_tree(
        self, clusters_tree: ClustersTree, cluster_type: str
    ) -> None:
        self.dbq.select(file=f"{cluster_type}_clusters").save(
            data=clusters_tree.clusters
        )
