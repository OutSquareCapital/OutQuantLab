import pandas as pd
import numpy as np
from scipy.stats import skew
import Config
from Process_Data import equity_curves_calculs
import Metrics as mt

def calculate_equity_curves_df(returns_df:pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame(equity_curves_calculs(returns_df.values),
                                 index=returns_df.index,
                                 columns=returns_df.columns,
                                 dtype=np.float32)

def calculate_overall_sharpe_ratio(returns_df: pd.DataFrame) -> pd.DataFrame:

    sharpe_ratios = returns_df.mean() / returns_df.std() * Config.ANNUALIZATION_FACTOR

    return pd.DataFrame(sharpe_ratios, 
                        columns=['Sharpe Ratio'], 
                        dtype=np.float32
                        ).round(2)

def calculate_overall_sortino_ratio(returns_df: pd.DataFrame) -> pd.DataFrame:

    mean_returns = returns_df.mean()
    
    downside_deviation = returns_df[returns_df < 0].std()
    
    sortino_ratios = mean_returns / downside_deviation * Config.ANNUALIZATION_FACTOR

    return pd.DataFrame(sortino_ratios, 
                        columns=['Sortino Ratio'], 
                        dtype=np.float32
                        ).round(2)

def calculate_average_correlation(returns_df: pd.DataFrame) -> pd.DataFrame:

    correlation_matrix = returns_df.corr()
    average_correlations = correlation_matrix.mean()

    return pd.DataFrame(average_correlations, 
                        columns=['Average Correlation'], 
                        dtype=np.float32
                        ).round(2)

def calculate_average_drawdown(returns_df: pd.DataFrame) -> pd.DataFrame:

    equity_curves = calculate_equity_curves_df(returns_df)
    
    # Calculate drawdowns for each equity curve directly
    drawdowns = (equity_curves - equity_curves.cummax()) / equity_curves.cummax() * Config.PERCENTAGE_FACTOR

    return drawdowns.mean().round(2)

def calculate_overall_sharpe_correlation_ratio(returns_df: pd.DataFrame) -> pd.DataFrame:

    sharpe_ratios_df = calculate_overall_sharpe_ratio(returns_df)
    average_correlations_df = calculate_average_correlation(returns_df)

    sharpe_ratios_df['Sharpe Rank'] = sharpe_ratios_df['Sharpe Ratio'].rank(method='min')
    average_correlations_df['Correlation Rank'] = average_correlations_df['Average Correlation'].rank(method='min')

    combined_df = pd.concat([sharpe_ratios_df, average_correlations_df], axis=1)

    combined_df['Sharpe/AvgCorrelation'] = combined_df['Sharpe Rank'] / combined_df['Correlation Rank']

    return combined_df

def calculate_overall_monthly_skew(returns_df: pd.DataFrame) -> pd.Series:

    monthly_returns_df = returns_df.resample('ME').mean()
    
    return monthly_returns_df.apply(lambda x: skew(x, nan_policy='omit')
                                    ).astype(np.float32
                                    ).round(2)

def calculate_overall_correlation_matrix(returns_df: pd.DataFrame):
    
    return returns_df.corr().round(2)

def calculate_rolling_sharpe_ratio(returns_df: pd.DataFrame, window_size: int = 1250):
        
        return pd.DataFrame(mt.rolling_sharpe_ratios(
                                                    returns_df.values, 
                                                    window_size, 
                                                    window_size),
                                                    index=returns_df.index,
                                                    columns=returns_df.columns
                                                    ).round(2)

def calculate_rolling_volatility(returns_df: pd.DataFrame, means: bool) -> pd.DataFrame:
    
    if means:
        rolling_volatility_df = pd.DataFrame(mt.hv_composite(returns_df.values), 
                                             index=returns_df.index, 
                                             columns=returns_df.columns)
        return rolling_volatility_df.expanding(min_periods=1).mean().round(2)
    else:
        return pd.DataFrame(mt.hv_composite(returns_df.values), 
                                             index=returns_df.index, 
                                             columns=returns_df.columns).round(2)

def calculate_drawdown(returns_df: pd.DataFrame) -> pd.DataFrame:

    equity_curves = calculate_equity_curves_df(returns_df)
    
    # Calculate drawdowns for each equity curve directly
    drawdowns = (equity_curves - equity_curves.cummax()) / equity_curves.cummax() * Config.PERCENTAGE_FACTOR

    return drawdowns.round(2)