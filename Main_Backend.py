import time
imports = time.perf_counter()
from Files import FILE_PATH_YF
from Get_Data import get_yahoo_finance_data
from Backtest import BacktestProcess
from Portfolio import calculate_daily_average_returns
from Config import AssetsCollection, IndicatorsCollection
from Dashboard import DashboardsCollection
print(f"Imports: {time.perf_counter() - imports:.2f}s")

#get_yahoo_finance_data(assets_collection.get_all_entities_names(), FILE_PATH_YF)

backtest_process_time = time.perf_counter()

assets_collection = AssetsCollection()
indicators_collection = IndicatorsCollection()
dashboards = DashboardsCollection(length=1250)

backtest = BacktestProcess(
file_path=FILE_PATH_YF,
asset_names=assets_collection.get_active_entities_names(),
indicators_and_params=indicators_collection.get_indicators_and_parameters_for_backtest()
)

raw_adjusted_returns_df = backtest.calculate_strategy_returns()

dashboards.sub_portfolios = calculate_daily_average_returns(
raw_adjusted_returns_df.dropna(axis=0),
by_method=True, 
by_asset=True)

dashboards.global_portfolio = calculate_daily_average_returns(
dashboards.sub_portfolios, 
global_avg=True
)
print(f"backtest process: {time.perf_counter() - backtest_process_time:.2f}s")

print(dashboards.calculate_metrics())
#assets_collection.save()
#indicators_collection.save()