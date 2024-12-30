from pandas import MultiIndex
from ConfigClasses.Indicators import Indicator
from Utilitary import ProgressFunc, DataFrameFloat
from Backtest import calculate_strategy_returns, aggregate_raw_returns
from Indicators import IndicatorsMethods
from ConfigClasses import AssetsCollection, IndicatorsCollection, ClustersTree, generate_multi_index_process
from Dashboard import DashboardsCollection
from Database import DataBaseQueries
def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc, database:DataBaseQueries) -> None:
        self.db: DataBaseQueries = database
        self.assets_collection = AssetsCollection(
            assets_to_test=self.db.load_json(db_file=self.db.assets_to_test), 
            asset_names=self.db.load_asset_names(db_file=self.db.price_data))
        self.indicators_collection = IndicatorsCollection(
            indicators_to_test=self.db.load_json(db_file=self.db.indics_to_test), 
            params_config=self.db.load_json(db_file=self.db.indics_params))
        self.assets_clusters = ClustersTree(clusters=self.db.load_json(db_file=self.db.assets_clusters))
        self.indicators_clusters = ClustersTree(clusters=self.db.load_json(db_file=self.db.indics_clusters))
        self.dashboards = DashboardsCollection(length=250)
        self.progress_callback = progress_callback
    def run_backtest(self) -> None:
        indics_methods = IndicatorsMethods()
        indicators_params: list[Indicator]=self.indicators_collection.indicators_params
        asset_names: list[str] = self.assets_collection.all_active_entities_names
        multi_index: MultiIndex = generate_multi_index_process(
            indicators_params=indicators_params, 
            asset_names=asset_names, 
            assets_clusters=self.assets_clusters, 
            indics_clusters=self.indicators_clusters)

        pct_returns_array, dates_index = self.db.load_prices(db_file=self.db.price_data, asset_names=asset_names)

        raw_adjusted_returns_df: DataFrameFloat= calculate_strategy_returns(
        pct_returns_array=pct_returns_array,
        indicators_params=indicators_params,
        indics_methods=indics_methods,
        dates_index=dates_index, 
        multi_index=multi_index, 
        progress_callback=self.progress_callback)

        self.dashboards.global_portfolio, self.dashboards.sub_portfolios = aggregate_raw_returns(
            raw_adjusted_returns_df=raw_adjusted_returns_df, 
            all_history=False
            )

    def save_all(self) -> None:
        self.db.save_json(db_file=self.db.assets_to_test, data=self.assets_collection.all_active_entities_dict, indent=3)
        self.db.save_json(db_file=self.db.indics_to_test, data=self.indicators_collection.all_active_entities_dict, indent=3)
        self.db.save_json(db_file=self.db.indics_params, data=self.indicators_collection.all_params_config, indent=3)
        self.db.save_json(db_file=self.db.indics_clusters, data=self.indicators_clusters.clusters, indent=3)
        self.db.save_json(db_file=self.db.assets_clusters, data=self.assets_clusters.clusters, indent=3)

if __name__ == "__main__":
        db = DataBaseQueries()
        outquantlab = OutQuantLab(progress_callback=handle_progress, database=db)
        outquantlab.run_backtest()
        print(outquantlab.dashboards.metrics)
        print(outquantlab.dashboards.all_plots_names)
        outquantlab.dashboards.plot(dashboard_name='Clusters Icicle', global_plot=False)