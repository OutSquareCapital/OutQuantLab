from Files import FILE_PATH_YF
from Get_Data import get_yahoo_finance_data
from Backtest import BacktestProcess
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
        self.backtest_process = BacktestProcess(
            file_path=FILE_PATH_YF,
            asset_names=self.assets_collection.get_active_entities_names(),
            asset_clusters=self.assets_collection.clusters,
            indics_clusters=self.indicators_collection.clusters,
            indicators_and_params=self.indicators_collection.get_indicators_and_parameters_for_backtest(),
            progress_callback=progress_callback
            )

    def run_backtest(self):
        raw_adjusted_returns_df = self.backtest_process.calculate_strategy_returns()
        self.dashboards.global_portfolio, self.dashboards.sub_portfolios = aggregate_raw_returns(raw_adjusted_returns_df)

    def refresh_data(self):
        get_yahoo_finance_data(self.assets_collection.get_all_entities_names(), FILE_PATH_YF)

    def close(self):
        self.assets_collection.save()
        self.indicators_collection.save()
        
if __name__ == "__main__":
    outquantlab = OutQuantLab(handle_progress)
    outquantlab.run_backtest()
    print(outquantlab.dashboards.calculate_metrics())