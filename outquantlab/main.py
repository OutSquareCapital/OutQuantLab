from outquantlab.backtest import Backtester
from outquantlab.config_classes import (
    Asset,
    AssetsClusters,
    AssetsCollection,
    IndicsClusters,
    IndicsCollection,
)
from outquantlab.database import DataBaseProvider
from outquantlab.graphs import GraphsCollection
from outquantlab.indicators import ReturnsData
from outquantlab.stats import BacktestStats
from outquantlab.typing_conventions import ProgressFunc


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.returns_data = ReturnsData(returns_df=self.dbp.get_initial_data())
        self.assets_collection: AssetsCollection = self.dbp.get_assets_collection()
        self.indics_collection: IndicsCollection = self.dbp.get_indics_collection(
            returns_data=self.returns_data
        )
        self.assets_clusters: AssetsClusters = self.dbp.get_assets_clusters_tree()
        self.indics_clusters: IndicsClusters = self.dbp.get_indics_clusters_tree()
        self.stats = BacktestStats(
            length=250,
            max_clusters=5,
            returns_limit=0.05,
            returns_data=self.returns_data,
        )
        self.graphs = GraphsCollection(stats=self.stats)

    def run(self, progress_callback: ProgressFunc) -> None:
        assets: list[Asset] = self.assets_collection.get_all_active_entities()
        self.returns_data.process_data(
            pct_returns_array=self.dbp.get_assets_returns(
                asset_names=[asset.name for asset in assets]
            )
        )

        Backtester(
            returns_data=self.returns_data,
            indics_params=self.indics_collection.get_indics_params(),
            assets=assets,
            indics_clusters=self.indics_clusters,
            assets_clusters=self.assets_clusters,
            progress_callback=progress_callback,
        )

    def save_all(self) -> None:
        self.dbp.save_assets_collection(assets_collection=self.assets_collection)
        self.dbp.save_indics_collection(indics_collection=self.indics_collection)
        self.dbp.save_assets_clusters_tree(clusters_tree=self.assets_clusters)
        self.dbp.save_indics_clusters_tree(clusters_tree=self.indics_clusters)
