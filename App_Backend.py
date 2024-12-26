from Files import FILE_PATH_YF, INDICATORS_CLUSTERS_FILE, ASSETS_CLUSTERS_FILE, ProgressFunc
from Backtest import calculate_strategy_returns, initialize_backtest_config, get_yahoo_finance_data
from Portfolio import aggregate_raw_returns
from Config import AssetsCollection, IndicatorsCollection, ClustersTree
from Dashboard import DashboardsCollection
import pandas as pd

def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc) -> None:
        self.assets_collection = AssetsCollection()
        self.indicators_collection = IndicatorsCollection()
        self.assets_clusters = ClustersTree(ASSETS_CLUSTERS_FILE)
        self.indicators_clusters = ClustersTree(INDICATORS_CLUSTERS_FILE)
        self.dashboards = DashboardsCollection(length=1250)
        self.progress_callback = progress_callback

    def run_backtest(self) -> None:
        backtest_data, backtest_config = initialize_backtest_config(
            file_path=FILE_PATH_YF,
            asset_names=self.assets_collection.all_active_entities_names,
            indicators_and_params=self.indicators_collection.indicators_params_dict,
            asset_clusters=self.assets_clusters,
            indics_clusters=self.indicators_clusters
        )

        raw_adjusted_returns_df:pd.DataFrame = calculate_strategy_returns(backtest_data, backtest_config, self.progress_callback)

        self.dashboards.global_portfolio, self.dashboards.sub_portfolios = aggregate_raw_returns(raw_adjusted_returns_df)

    def refresh_data(self) -> None:
        get_yahoo_finance_data(self.assets_collection.all_entities_names, FILE_PATH_YF)

    def close(self) -> None:
        self.assets_collection.save()
        self.indicators_collection.save()

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    outquantlab = OutQuantLab(handle_progress)
    outquantlab.run_backtest()
    print(outquantlab.dashboards.calculate_metrics())
    end = time.perf_counter() - start
    print(f"Time taken: {end:.2f} seconds")