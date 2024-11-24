import Config
from Signals import *
import Portfolio
import Get_Data
import Process_Data
import Dashboard
import Backtest

# Re-actualisation du data
#Get_Data.get_yahoo_finance_data(Config.yahoo_assets, Config.FILE_PATH_YF)

data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Config.FILE_PATH_YF)

indicators_and_params, assets_to_backtest = Config.dynamic_config(assets_names, auto=True)

(prices_array, 
volatility_adjusted_pct_returns_array, 
log_returns_array, 
category_asset_names,
dates_index
) = Process_Data.process_data(assets_names,
                            data_prices_df, 
                            assets_to_backtest)

del (
    assets_to_backtest,
    data_prices_df, 
    assets_names
    )

raw_adjusted_returns_df = Backtest.process_backtest(prices_array,
                                                    log_returns_array,
                                                    volatility_adjusted_pct_returns_array,
                                                    category_asset_names,
                                                    dates_index,
                                                    indicators_and_params)

del (
    prices_array,
    log_returns_array,
    volatility_adjusted_pct_returns_array,
    dates_index,
    category_asset_names,
    indicators_and_params
    )

#portfolio_base_structure = Portfolio.classify_assets(asset_names_test, Config.portfolio_etf)

#relativized_sharpes_df = Portfolio.relative_sharpe_on_confidence_period(raw_adjusted_returns_df, sharpe_lookback = 5000, confidence_lookback=2500)
#optimized_returns_rltv = raw_adjusted_returns_df * relativized_sharpes_df.shift(1)
#test_strategy_returns = Portfolio.calculate_daily_average_returns(optimized_returns_rltv, by_method=True, by_class=True, by_asset=True)
#test_asset_returns = Portfolio.generate_recursive_strategy_means(test_strategy_returns, Config.portfolio_strategies)
#test_global_returns = Portfolio.generate_recursive_means(test_asset_returns, portfolio_base_structure)
#test_global_returns = test_global_returns.rename(columns={test_global_returns.columns[0]: 'cluster_optimized'})

equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'equal_weights'})

# Concaténation des DataFrames
#total_df = pd.concat([test_global_returns, equal_weights_global_returns], axis=1).dropna()

test_returns = equal_weights_asset_returns#.loc['2015-01-01':]

#Dashboard.plot_equity(test_returns)
Dashboard.plot_drawdowns(test_returns)
#Dashboard.plot_rolling_volatility(test_returns)
#Dashboard.plot_rolling_sharpe_ratio(test_returns)

#Dashboard.plot_overall_sharpe_ratio(test_returns)
#Dashboard.plot_average_drawdown(test_returns)
#Dashboard.plot_overall_monthly_skew(test_returns)
#Dashboard.plot_average_inverted_correlation(test_returns)
#Dashboard.plot_overall_sharpe_correlation_ratio(test_returns)

#Dashboard.plot_correlation_heatmap(test_returns)
#Dashboard.plot_sharpe_ratio_heatmap(raw_adjusted_returns_df, 'LenST', 'LenLT')

#Dashboard.plot_returns_distribution_violin(test_returns, limit=0.00001)
Dashboard.plot_returns_distribution_histogram(test_returns, limit=0.000001)
#Dashboard.plot_overall_sharpe_ratio_3d_scatter(raw_adjusted_returns_df, ['LenST', 'LenLT', 'MacdLength'])
#Dashboard.plot_static_clusters(test_returns, 6, 2, 1)