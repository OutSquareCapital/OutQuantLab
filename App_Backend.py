from pandas import MultiIndex
from Utilitary import ProgressFunc, DataFrameFloat
from Backtest import calculate_strategy_returns, aggregate_raw_returns
from Indicators import IndicatorsMethods
from ConfigClasses import AssetsCollection, IndicatorsCollection, ClustersTree, generate_multi_index_process
from Graphs import GraphsCollection
from DataBase import DataBaseQueries
def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc) -> None:
        self.global_portfolio: DataFrameFloat
        self.sub_portfolios: DataFrameFloat
        self.db: DataBaseQueries = DataBaseQueries()
        self.assets_collection = AssetsCollection(
            assets_to_test=self.db.select['assets_to_test'].load_json(), 
            asset_names=self.db.select['price_data'].load_asset_names())
        self.indicators_collection = IndicatorsCollection(
            indicators_to_test=self.db.select['indics_to_test'].load_json(), 
            params_config=self.db.select['indics_params'].load_json()
            )
        self.assets_clusters = ClustersTree(clusters=self.db.select['assets_clusters'].load_json())
        self.indicators_clusters = ClustersTree(clusters=self.db.select['indics_clusters'].load_json())
        self.grph = GraphsCollection(length=250, max_clusters=5, returns_limit=0.05)
        self.progress_callback = progress_callback
    def run_backtest(self) -> None:
        indics_methods = IndicatorsMethods()
        multi_index: MultiIndex = generate_multi_index_process(
            indicators_params=self.indicators_collection.indicators_params, 
            asset_names=self.assets_collection.all_active_entities_names, 
            assets_clusters=self.assets_clusters, 
            indics_clusters=self.indicators_clusters)

        (
        pct_returns_array, 
        dates_index
        ) = self.db.select['price_data'].load_prices(asset_names=self.assets_collection.all_active_entities_names)

        raw_adjusted_returns_df: DataFrameFloat= calculate_strategy_returns(
        pct_returns_array=pct_returns_array,
        indicators_params=self.indicators_collection.indicators_params,
        indics_methods=indics_methods,
        dates_index=dates_index, 
        multi_index=multi_index, 
        progress_callback=self.progress_callback)

        self.global_portfolio, self.sub_portfolios = aggregate_raw_returns(
            raw_adjusted_returns_df=raw_adjusted_returns_df, 
            all_history=False
            )

    def save_all(self) -> None:
        self.db.select['assets_to_test'].save_json(data=self.assets_collection.all_active_entities_dict)
        self.db.select['indics_to_test'].save_json(data=self.indicators_collection.all_active_entities_dict)
        self.db.select['indics_params'].save_json(data=self.indicators_collection.all_params_config)
        self.db.select['indics_clusters'].save_json(data=self.indicators_clusters.clusters)
        self.db.select['assets_clusters'].save_json(data=self.assets_clusters.clusters)

if __name__ == "__main__":
        oql = OutQuantLab(progress_callback=handle_progress)
        oql.run_backtest()
        print(oql.grph.get_metrics(returns_df=oql.global_portfolio))
        oql.grph.plot_clusters_icicle(returns_df=oql.sub_portfolios, show_legend=False, as_html=False)