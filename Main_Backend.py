import time
from Files import FILE_PATH_YF
from Get_Data import get_yahoo_finance_data
from Backtest import BacktestProcess
from Portfolio import calculate_portfolio_returns
from Config import AssetsCollection, IndicatorsCollection
from Dashboard import DashboardsCollection

#get_yahoo_finance_data(assets_collection.get_all_entities_names(), FILE_PATH_YF)

backtest_process_time = time.perf_counter()

assets_collection = AssetsCollection()
indicators_collection = IndicatorsCollection()
dashboards = DashboardsCollection(length=1250)
backtest_process = BacktestProcess(
    file_path=FILE_PATH_YF,
    asset_names=assets_collection.get_active_entities_names(),
    indicators_and_params=indicators_collection.get_indicators_and_parameters_for_backtest()
    )

raw_adjusted_returns_df = backtest_process.calculate_strategy_returns()

indics_assets_portfolio = calculate_portfolio_returns(
    raw_adjusted_returns_df.dropna(axis=0),
    by_asset=True,
    by_indic=True
    )

dashboards.sub_portfolios = calculate_portfolio_returns(
    indics_assets_portfolio,
    by_asset=True
    )

dashboards.global_portfolio = calculate_portfolio_returns(dashboards.sub_portfolios)

print(f"backtest process: {time.perf_counter() - backtest_process_time:.2f}s")
print(dashboards.calculate_metrics())
#assets_collection.save()
#indicators_collection.save()