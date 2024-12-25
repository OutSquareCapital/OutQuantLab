from Files import FILE_PATH_YF
from Backtest import calculate_strategy_returns, initialize_backtest_config, get_yahoo_finance_data
from Portfolio import aggregate_raw_returns
from Config import AssetsCollection, IndicatorsCollection
from Dashboard import DashboardsCollection
from collections.abc import Callable

def handle_progress(progress: int, message: str):
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: Callable):
        self.assets_collection = AssetsCollection()
        self.indicators_collection = IndicatorsCollection()
        self.dashboards = DashboardsCollection(length=1250)
        self.progress_callback = progress_callback

    def run_backtest(self):

        backtest_data, backtest_config = initialize_backtest_config(
            file_path=FILE_PATH_YF,
            asset_names=self.assets_collection.all_active_entities_names,
            indicators_and_params=self.indicators_collection.indicators_params_dict,
            asset_clusters=self.assets_collection.clusters,
            indics_clusters=self.indicators_collection.clusters
        )

        raw_adjusted_returns_df = calculate_strategy_returns(backtest_data, backtest_config, self.progress_callback)

        self.dashboards.global_portfolio, self.dashboards.sub_portfolios = aggregate_raw_returns(raw_adjusted_returns_df)

    def refresh_data(self):
        get_yahoo_finance_data(self.assets_collection.all_entities_names, FILE_PATH_YF)

    def close(self):
        self.assets_collection.save()
        self.indicators_collection.save()

if __name__ == "__main__":
    outquantlab = OutQuantLab(handle_progress)
    outquantlab.run_backtest()
    print(outquantlab.dashboards.calculate_metrics())