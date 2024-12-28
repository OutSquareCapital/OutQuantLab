from Utilitary import ProgressFunc
from Database import CONFIG
from Backtest import calculate_strategy_returns, generate_multi_index_process
from Portfolio import aggregate_raw_returns
from Indicators import IndicatorsMethods
from Config import AssetsCollection, IndicatorsCollection, ClustersTree
from Dashboard import DashboardsCollection

def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc) -> None:
        self.assets_collection = AssetsCollection(CONFIG.assets_to_test, CONFIG.price_data)
        self.indicators_collection = IndicatorsCollection(CONFIG.indics_to_test, CONFIG.indics_params)
        self.assets_clusters = ClustersTree(CONFIG.assets_clusters)
        self.indicators_clusters = ClustersTree(CONFIG.indics_clusters)
        self.dashboards = DashboardsCollection(length=1250)
        self.progress_callback = progress_callback
    def run_backtest(self) -> None:
        indics_methods = IndicatorsMethods()
        indicators_params=self.indicators_collection.indicators_params
        asset_names = self.assets_collection.all_active_entities_names
        multi_index = generate_multi_index_process(
            indicators_params, 
            asset_names, 
            self.assets_clusters, 
            self.indicators_clusters)

        pct_returns_array, dates_index = load_prices(asset_names, CONFIG.price_data)

        raw_adjusted_returns_df= calculate_strategy_returns(
        pct_returns_array,
        indicators_params,
        indics_methods,
        dates_index, 
        multi_index, 
        self.progress_callback)

        self.dashboards.global_portfolio, self.dashboards.sub_portfolios = aggregate_raw_returns(raw_adjusted_returns_df, all_history=False)

    def refresh_data(self) -> None:
        get_yahoo_finance_data(self.assets_collection.all_entities_names, CONFIG.price_data)

    def close(self) -> None:
        self.assets_collection.save()
        self.indicators_collection.save()

if __name__ == "__main__":

        outquantlab = OutQuantLab(handle_progress)
        outquantlab.run_backtest()
        print(outquantlab.dashboards.calculate_metrics())