from pandas import MultiIndex

from database import DataBaseProvider
from backtest import aggregate_raw_returns, calculate_strategy_returns
from config_classes import (
    AssetsCollection,
    ClustersTree,
    IndicatorsCollection,
    generate_overall_clusters_structure,
    generate_multi_index_process,
)
from stats import BacktestStats
from typing_conventions import DataFrameFloat, ProgressFunc
from indicators import BaseIndicator, ReturnsData


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.assets_collection: AssetsCollection = self.dbp.get_assets_collection()
        self.returns_data = ReturnsData(returns_df=self.dbp.get_initial_data())
        self.indics_collection: IndicatorsCollection = (
            self.dbp.get_indicators_collection(returns_data=self.returns_data)
        )
        self.assets_clusters: ClustersTree = self.dbp.get_clusters_tree(
            cluster_type="assets"
        )
        self.indics_clusters: ClustersTree = self.dbp.get_clusters_tree(
            cluster_type="indics"
        )
        self.stats = BacktestStats(
            length=250, max_clusters=5, returns_limit=0.05, returns_data=self.returns_data
        )

    def execute_backtest(self, progress_callback: ProgressFunc) -> None:
        
        asset_names: list[str] = self.assets_collection.all_active_entities_names
        indics_params: list[BaseIndicator] = self.indics_collection.indicators_params
        clusters_structure: list[str] = generate_overall_clusters_structure(
            indic_clusters_structure=self.indics_clusters.clusters_structure,
            asset_clusters_structure=self.assets_clusters.clusters_structure,
        )
        multi_index: MultiIndex = generate_multi_index_process(
            clusters_structure=clusters_structure,
            indicators_params=indics_params,
            asset_names=asset_names,
            assets_to_clusters=self.assets_clusters.map_nested_clusters_to_entities(),
            indics_to_clusters=self.indics_clusters.map_nested_clusters_to_entities(),
        )
        self.returns_data.process_data(pct_returns_array=self.dbp.get_assets_returns(asset_names=asset_names))

        raw_adjusted_returns_df: DataFrameFloat = calculate_strategy_returns(
            returns_data=self.returns_data,
            indicators_params=indics_params,
            multi_index=multi_index,
            progress_callback=progress_callback,
        )
        (
            self.returns_data.global_returns,
            self.returns_data.sub_portfolio_roll,
            self.returns_data.sub_portfolio_ovrll,
        ) = aggregate_raw_returns(
            raw_adjusted_returns_df=raw_adjusted_returns_df,
            clusters_structure=clusters_structure,
            all_history=True,
            progress_callback=progress_callback,
        )

    def save_all(self) -> None:
        self.dbp.save_assets_collection(assets_collection=self.assets_collection)
        self.dbp.save_indicators_collection(indics_collection=self.indics_collection)
        self.dbp.save_clusters_tree(
            clusters_tree=self.assets_clusters, cluster_type="assets"
        )
        self.dbp.save_clusters_tree(
            clusters_tree=self.indics_clusters, cluster_type="indics"
        )
