from pandas import MultiIndex
from ConfigClasses.Indicators import Indicator
from Utilitary import ProgressFunc, DataFrameFloat
from Database import CONFIG, load_asset_names, load_prices, get_yahoo_finance_data, load_config_file, save_config_file
from Backtest import calculate_strategy_returns, aggregate_raw_returns
from Indicators import IndicatorsMethods
from ConfigClasses import AssetsCollection, IndicatorsCollection, ClustersTree, generate_multi_index_process
from Dashboard import DashboardsCollection

asset_to_test = load_config_file(file_path=CONFIG.assets_to_test)
asset_names = load_asset_names(file_path=CONFIG.price_data)
indicators_to_test=load_config_file(file_path=CONFIG.indics_to_test)
params_config  = load_config_file(file_path=CONFIG.indics_params)
assets_clusters = load_config_file(file_path=CONFIG.assets_clusters)
indicators_clusters = load_config_file(file_path=CONFIG.indics_clusters)

def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc) -> None:
        self.assets_collection = AssetsCollection(assets_to_test=asset_to_test, assets_data=asset_names)
        self.indicators_collection = IndicatorsCollection(indicators_to_test=indicators_to_test, params_config=params_config)
        self.assets_clusters = ClustersTree(clusters=assets_clusters)
        self.indicators_clusters = ClustersTree(clusters=indicators_clusters)
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
        save_config_file(file_path=CONFIG.assets_to_test, dict_to_save=self.assets_collection.all_active_entities_dict, indent=3)
        save_config_file(file_path=CONFIG.indics_to_test, dict_to_save=self.indicators_collection.all_active_entities_dict, indent=3)
        save_config_file(file_path=CONFIG.indics_params, dict_to_save=self.indicators_collection.all_params_config, indent=3)
        save_config_file(file_path=CONFIG.indics_clusters, dict_to_save=self.indicators_clusters.clusters, indent=3)
        save_config_file(file_path=CONFIG.assets_clusters, dict_to_save=self.assets_clusters.clusters, indent=3)
        
if __name__ == "__main__":

        outquantlab = OutQuantLab(progress_callback=handle_progress)
        outquantlab.run_backtest()
        #print(outquantlab.dashboards.metrics)
        #outquantlab.dashboards.plot(dashboard_name='Rolling Average Correlation').show()
        #outquantlab.dashboards.plot(dashboard_name='Clusters Icicle').show()