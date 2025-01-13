from pandas import MultiIndex

from Backtest import aggregate_raw_returns, calculate_strategy_returns
from ConfigClasses import (
    AssetsCollection,
    ClustersTree,
    IndicatorsCollection,
    generate_clusters_structure,
    generate_multi_index_process
)
from ConfigClasses.Indicators import Indicator
from DataBase import DataBaseQueries
from Graphs import GraphsCollection
from Indicators import IndicatorsMethods
from TypingConventions import DataFrameFloat, ProgressFunc

class OutQuantLab:
    def __init__(
        self, progress_callback: ProgressFunc, database: DataBaseQueries
    ) -> None:
        self.db: DataBaseQueries = database
        self.assets_collection = AssetsCollection(
            assets_to_test=self.db.select["assets_to_test"].load(),
            asset_names=self.db.select["price_data"].load_asset_names(),
        )
        self.indics_collection = IndicatorsCollection(
            indicators_to_test=self.db.select["indics_to_test"].load(),
            params_config=self.db.select["indics_params"].load(),
        )
        self.assets_clusters = ClustersTree(
            clusters=self.db.select["assets_clusters"].load(), prefix="Asset"
        )
        self.indics_clusters = ClustersTree(
            clusters=self.db.select["indics_clusters"].load(), prefix="Indic"
        )
        self.initial_df: DataFrameFloat = self.db.select[
            "price_data"
        ].load_initial_data()
        self.grphs = GraphsCollection(
            length=250, max_clusters=5, returns_limit=0.05, initial_data=self.initial_df
        )
        self.progress_callback = progress_callback


    def run_backtest(self) -> None:
        asset_names: list[str] = self.assets_collection.all_active_entities_names
        indics_params: list[Indicator] = self.indics_collection.indicators_params
        clusters_structure: list[str] = generate_clusters_structure(
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


        raw_adjusted_returns_df: DataFrameFloat = calculate_strategy_returns(
            pct_returns_array=self.db.select["price_data"].load_returns(
                asset_names=asset_names
            ),
            indicators_params=indics_params,
            indics_methods=IndicatorsMethods(),
            dates_index=self.initial_df.dates,
            multi_index=multi_index,
            progress_callback=self.progress_callback,
        )


        (
            self.grphs.global_returns,
            self.grphs.sub_portfolio_roll,
            self.grphs.sub_portfolio_ovrll,
        ) = aggregate_raw_returns(
            raw_adjusted_returns_df=raw_adjusted_returns_df,
            clusters_structure=clusters_structure,
            all_history=True,
            progress_callback=self.progress_callback,
        )


    def save_all(self) -> None:
        self.db.select["assets_to_test"].save(
            data=self.assets_collection.all_active_entities_dict
        )
        self.db.select["indics_to_test"].save(
            data=self.indics_collection.all_active_entities_dict
        )
        self.db.select["indics_params"].save(
            data=self.indics_collection.all_params_config
        )
        self.db.select["indics_clusters"].save(
            data=self.indics_clusters.clusters
        )
        self.db.select["assets_clusters"].save(
            data=self.assets_clusters.clusters
        )