from pandas import MultiIndex
from ConfigClasses.Indicators import Indicator
from Utilitary import ProgressFunc
from Database import CONFIG, load_prices, get_yahoo_finance_data
from Backtest import calculate_strategy_returns, aggregate_raw_returns
from Indicators import IndicatorsMethods
from ConfigClasses import AssetsCollection, IndicatorsCollection, ClustersTree, generate_multi_index_process
from Dashboard import DashboardsCollection
from Utilitary import DataFrameFloat

def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc) -> None:
        self.assets_collection = AssetsCollection(assets_to_test=CONFIG.assets_to_test, assets_data=CONFIG.price_data)
        self.indicators_collection = IndicatorsCollection(indicators_to_test=CONFIG.indics_to_test, indicators_params=CONFIG.indics_params)
        self.assets_clusters = ClustersTree(clusters_file=CONFIG.assets_clusters)
        self.indicators_clusters = ClustersTree(clusters_file=CONFIG.indics_clusters)
        self.dashboards = DashboardsCollection(length=1250)
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

        pct_returns_array, dates_index = load_prices(asset_names=asset_names, file_path=CONFIG.price_data)

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

    def refresh_data(self) -> None:
        get_yahoo_finance_data(assets=self.assets_collection.all_entities_names, file_path=CONFIG.price_data)

    def close(self) -> None:
        self.assets_collection.save()
        self.indicators_collection.save()

if __name__ == "__main__":

        outquantlab = OutQuantLab(progress_callback=handle_progress)
        outquantlab.run_backtest()
        print(outquantlab.dashboards.metrics)