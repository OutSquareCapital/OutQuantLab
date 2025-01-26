from outquantlab.backtest import execute_backtest
from outquantlab.config_classes import (
    AssetsClusters,
    AssetsCollection,
    IndicsClusters,
    IndicsCollection,
)
from outquantlab.database import DataBaseProvider
from outquantlab.graphs import GraphsCollection
from outquantlab.indicators import DataDfs


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.assets_collection: AssetsCollection = self.dbp.get_assets_collection()
        self.indics_collection: IndicsCollection = self.dbp.get_indics_collection()
        self.assets_clusters: AssetsClusters = self.dbp.get_assets_clusters_tree()
        self.indics_clusters: IndicsClusters = self.dbp.get_indics_clusters_tree()

    def run(self) -> GraphsCollection:
        data_dfs: DataDfs = self.dbp.get_initial_data()
        execute_backtest(
            data_dfs=data_dfs,
            indics_params=self.indics_collection.get_indics_params(),
            assets=self.assets_collection.get_all_active_entities(),
            indics_clusters=self.indics_clusters,
            assets_clusters=self.assets_clusters,
        )
        print(data_dfs.global_returns)
        return GraphsCollection(data_dfs=data_dfs)

    def save_all(self) -> None:
        self.dbp.save_all(
            assets_collection=self.assets_collection,
            indics_collection=self.indics_collection,
            assets_clusters=self.assets_clusters,
            indics_clusters=self.indics_clusters,
        )
