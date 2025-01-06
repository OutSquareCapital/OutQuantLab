from ConfigClasses.Indicators import Indicator
from Utilitary import ProgressFunc, DataFrameFloat, APP_NAME
from Backtest import calculate_strategy_returns, aggregate_raw_returns
from Indicators import IndicatorsMethods
from ConfigClasses import AssetsCollection, IndicatorsCollection, ClustersTree, generate_multi_index_process
from Graphs import GraphsCollection
from DataBase import DataBaseQueries
from pandas import MultiIndex

class OutQuantLabCLI:
    def __init__(self) -> None:
        self.oql: OutQuantLab = OutQuantLab(
            progress_callback=self.handle_progress,
            database=DataBaseQueries()
        )
        print(f"{APP_NAME} initialized")
        self.run()

    def handle_progress(self, progress: int, message: str) -> None:
        pass
        #print(f"[{progress}%] {message}")

    def run(self) -> None:
        import time
        start = time.perf_counter()
        for _ in range(10):
            self.oql.run_backtest()
            print(f'{_} on {10}')
        end: float = time.perf_counter() - start
        print(f'time: {end:.2f}')
        metrics: dict[str, float] = self.oql.grphs.get_metrics()
        for metric, value in metrics.items():
            print(f"{metric}: {value}")
        
class OutQuantLab:
    def __init__(self, progress_callback: ProgressFunc, database: DataBaseQueries) -> None:
        self.db: DataBaseQueries = database
        self.assets_collection = AssetsCollection(
            assets_to_test=self.db.select['assets_to_test'].load_json(), 
            asset_names=self.db.select['price_data'].load_asset_names())
        self.indics_collection = IndicatorsCollection(
            indicators_to_test=self.db.select['indics_to_test'].load_json(), 
            params_config=self.db.select['indics_params'].load_json()
            )
        self.assets_clusters = ClustersTree(clusters=self.db.select['assets_clusters'].load_json())
        self.indics_clusters = ClustersTree(clusters=self.db.select['indics_clusters'].load_json())
        self.initial_df: DataFrameFloat = self.db.select['price_data'].load_initial_data()
        self.grphs = GraphsCollection(
            length=250, 
            max_clusters=5, 
            returns_limit=0.05, 
            initial_data=self.initial_df
            )
        self.progress_callback = progress_callback

    def run_backtest(self) -> None:
        indics_methods = IndicatorsMethods()
        asset_names: list[str] = self.assets_collection.all_active_entities_names
        clusters_structure: list[str] = ["AssetCluster", "AssetSubCluster", "Asset", "IndicCluster", "IndicSubCluster", "Indicator", "Param"]
        indics_params: list[Indicator] = self.indics_collection.indicators_params

        multi_index: MultiIndex = generate_multi_index_process(
            clusters_structure=clusters_structure,
            indicators_params=indics_params, 
            asset_names=asset_names, 
            assets_to_clusters=self.assets_clusters.map_nested_clusters_to_entities(), 
            indics_to_clusters=self.indics_clusters.map_nested_clusters_to_entities()
            )

        raw_adjusted_returns_df: DataFrameFloat = calculate_strategy_returns(
        pct_returns_array=self.db.select['price_data'].load_returns(asset_names=asset_names),
        indicators_params=indics_params,
        indics_methods=indics_methods,
        dates_index=self.initial_df.dates, 
        multi_index=multi_index, 
        progress_callback=self.progress_callback)

        self.grphs.global_returns, self.grphs.sub_portfolio_roll, self.grphs.sub_portfolio_ovrll = aggregate_raw_returns(
            raw_adjusted_returns_df=raw_adjusted_returns_df,
            clusters_structure=clusters_structure,
            all_history=True,
            progress_callback=self.progress_callback
            )

    def save_all(self) -> None:
        self.db.select['assets_to_test'].save_json(data=self.assets_collection.all_active_entities_dict)
        self.db.select['indics_to_test'].save_json(data=self.indics_collection.all_active_entities_dict)
        self.db.select['indics_params'].save_json(data=self.indics_collection.all_params_config)
        self.db.select['indics_clusters'].save_json(data=self.indics_clusters.clusters)
        self.db.select['assets_clusters'].save_json(data=self.assets_clusters.clusters)