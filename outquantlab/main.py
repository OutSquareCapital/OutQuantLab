from pandas import MultiIndex

from outquantlab.backtest import (
    BacktestSpecs,
    aggregate_raw_returns,
    process_strategies,
)
from outquantlab.config_classes import (
    Asset,
    AssetsClusters,
    AssetsCollection,
    IndicatorsCollection,
    IndicsClusters,
    generate_multi_index_process,
)
from outquantlab.database import DataBaseProvider
from outquantlab.graphs import GraphsCollection
from outquantlab.indicators import BaseIndicator, ReturnsData
from outquantlab.stats import BacktestStats
from outquantlab.typing_conventions import ArrayFloat, ProgressFunc


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.assets_collection: AssetsCollection = self.dbp.get_assets_collection()
        self.returns_data = ReturnsData(returns_df=self.dbp.get_initial_data())
        self.indics_collection: IndicatorsCollection = (
            self.dbp.get_indicators_collection(returns_data=self.returns_data)
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
        indics_params: list[BaseIndicator] = self.indics_collection.get_indics_params()
        assets: list[Asset] = self.assets_collection.get_all_active_entities()
        self.returns_data.process_data(
            pct_returns_array=self.dbp.get_assets_returns(
                asset_names=[asset.name for asset in assets]
            )
        )

        multi_index: MultiIndex = generate_multi_index_process(
            indic_param_tuples=self.indics_clusters.get_clusters_tuples(
                entities=indics_params
            ),
            asset_tuples=self.assets_clusters.get_clusters_tuples(entities=assets),
        )
        backtest_specs: BacktestSpecs = BacktestSpecs(
            returns_data=self.returns_data,
            indics_params=indics_params,
            multi_index=multi_index,
        )
        signals_array: ArrayFloat = process_strategies(
            indics_params=indics_params,
            backtest_specs=backtest_specs,
            progress_callback=progress_callback,
        )
        (
            self.returns_data.global_returns,
            self.returns_data.sub_portfolio_roll,
            self.returns_data.sub_portfolio_ovrll,
        ) = aggregate_raw_returns(
            signals_array=signals_array,
            backtest_specs=backtest_specs,
            progress_callback=progress_callback,
        )

    def save_all(self) -> None:
        self.dbp.save_assets_collection(assets_collection=self.assets_collection)
        self.dbp.save_indics_collection(indics_collection=self.indics_collection)
        self.dbp.save_assets_clusters_tree(clusters_tree=self.assets_clusters)
        self.dbp.save_indics_clusters_tree(clusters_tree=self.indics_clusters)
