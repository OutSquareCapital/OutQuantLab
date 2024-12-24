from Files import FILE_PATH_YF
from Get_Data import get_yahoo_finance_data
from Backtest import BacktestProcess
from Portfolio import aggregate_raw_returns
from Config import AssetsCollection, IndicatorsCollection
from Dashboard import DashboardsCollection

#get_yahoo_finance_data(assets_collection.get_all_entities_names(), FILE_PATH_YF)

assets_collection = AssetsCollection()
indicators_collection = IndicatorsCollection()
dashboards = DashboardsCollection(length=1250)
backtest_process = BacktestProcess(
    file_path=FILE_PATH_YF,
    asset_names=assets_collection.get_active_entities_names(),
    indicators_and_params=indicators_collection.get_indicators_and_parameters_for_backtest(),
    asset_clusters=assets_collection.clusters,
    indics_clusters=indicators_collection.clusters
    )

raw_adjusted_returns_df = backtest_process.calculate_strategy_returns()

dashboards.global_portfolio, dashboards.sub_portfolios = aggregate_raw_returns(raw_adjusted_returns_df)

print(dashboards.calculate_metrics())

#assets_collection.save()
#indicators_collection.save()