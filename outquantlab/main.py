from outquantlab.backtest import Backtester
from outquantlab.config_classes import (
    AssetsClusters,
    AssetsCollection,
    IndicsClusters,
    IndicsCollection,
)
from outquantlab.database import DataBaseProvider
from outquantlab.graphs import GraphsCollection
from outquantlab.indicators import DataArrays, DataDfs
from outquantlab.stats import BacktestStats


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.data_dfs = DataDfs(returns_df=self.dbp.get_initial_data())
        self.datas_arrays = DataArrays(
            returns_array=self.data_dfs.global_returns.get_array()
        )
        self.assets_collection: AssetsCollection = self.dbp.get_assets_collection()
        self.indics_collection: IndicsCollection = self.dbp.get_indics_collection(
            data_arrays=self.datas_arrays
        )
        self.assets_clusters: AssetsClusters = self.dbp.get_assets_clusters_tree()
        self.indics_clusters: IndicsClusters = self.dbp.get_indics_clusters_tree()
        self.stats = BacktestStats(
            length=250,
            max_clusters=5,
            returns_limit=0.05,
            data_dfs=self.data_dfs,
        )
        self.graphs = GraphsCollection(stats=self.stats)

    def run(self) -> None:
        Backtester(
            data_arrays=self.datas_arrays,
            data_dfs=self.data_dfs,
            indics_params=self.indics_collection.get_indics_params(),
            assets=self.assets_collection.get_all_active_entities(),
            indics_clusters=self.indics_clusters,
            assets_clusters=self.assets_clusters,
        )

    def save_all(self) -> None:
        self.dbp.save_assets_collection(assets_collection=self.assets_collection)
        self.dbp.save_indics_collection(indics_collection=self.indics_collection)
        self.dbp.save_assets_clusters_tree(clusters_tree=self.assets_clusters)
        self.dbp.save_indics_clusters_tree(clusters_tree=self.indics_clusters)
