from Files import FILE_PATH_YF
from Get_Data import get_yahoo_finance_data
from Process_Data import BacktestConfig
from Backtest import process_backtest
import Portfolio
from Config import AssetsCollection, IndicatorsCollection
from Dashboard import DashboardsCollection

#get_yahoo_finance_data(assets_collection.get_all_entities_names(), FILE_PATH_YF)

def handle_progress(progress: int, message: str):
    print(f"[{progress}%] {message}")

assets_collection = AssetsCollection()
indicators_collection = IndicatorsCollection()
dashboards = DashboardsCollection(length=1250)

config = BacktestConfig(
FILE_PATH_YF,
assets_collection.get_active_entities_names(),
indicators_collection.get_indicators_and_parameters_for_backtest()
)

raw_adjusted_returns_df = process_backtest(
config.signals_array,
config.data_array,
config.volatility_adjusted_pct_returns,
config.dates_index,
config.indicators_and_params,
config.multi_index,
handle_progress
)

dashboards.sub_portfolios = Portfolio.calculate_daily_average_returns(
raw_adjusted_returns_df.dropna(axis=0),
by_method=True, 
by_asset=True)

dashboards.global_portfolio = Portfolio.calculate_daily_average_returns(
dashboards.sub_portfolios, 
global_avg=True
)

#assets_collection.save()
#indicators_collection.save()