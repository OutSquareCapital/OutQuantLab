import pandas as pd
import numpy as np
from scipy.stats import skew
import Config
from Process_Data import equity_curves_calculs
import Metrics as mt
import Config

def calculate_equity_curves_df(returns_df: pd.DataFrame):

    return pd.DataFrame(equity_curves_calculs(returns_df.values),
                                              index=returns_df.index,
                                              columns=returns_df.columns,
                                              dtype=np.float32
                                              ).round(2)

def calculate_overall_volatility(returns_df: pd.DataFrame) -> pd.DataFrame:

    volatility = returns_df.std() * Config.ANNUALIZED_PERCENTAGE_FACTOR

    return pd.DataFrame(volatility, 
                        columns=['Volatility'], 
                        dtype=np.float32
                        ).round(2)

def calculate_overall_sharpe_ratio(returns_df: pd.DataFrame) -> pd.DataFrame:

    sharpe_ratios = returns_df.mean() / returns_df.std() * Config.ANNUALIZATION_FACTOR

    return pd.DataFrame(sharpe_ratios, 
                        columns=['Sharpe Ratio'], 
                        dtype=np.float32
                        ).round(2)

def calculate_overall_average_correlation(returns_df: pd.DataFrame) -> pd.DataFrame:

    correlation_matrix = returns_df.corr()
    average_correlations = correlation_matrix.mean()

    return pd.DataFrame(average_correlations, 
                        columns=['Average Correlation'], 
                        dtype=np.float32
                        ).round(2)

def calculate_overall_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:

    return returns_df.corr().round(2)

def calculate_overall_average_drawdown(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:

    return calculate_rolling_drawdown(returns_df, length).mean().round(2)

def format_returns(returns_df: pd.DataFrame, limit: int) -> pd.DataFrame:
    lower_threshold = returns_df.quantile(limit, axis=0)
    upper_threshold = returns_df.quantile(1-limit, axis=0)
    
    formatted_returns_df = returns_df.where((returns_df >= lower_threshold) & (returns_df <= upper_threshold), np.nan)
    formatted_returns_df = formatted_returns_df * Config.PERCENTAGE_FACTOR

    return formatted_returns_df.round(2)

def calculate_overall_monthly_skew(returns_df: pd.DataFrame) -> pd.Series:

    monthly_returns_df = returns_df.resample('ME').mean()
    
    return monthly_returns_df.apply(lambda x: skew(x, nan_policy='omit')
                                    ).astype(np.float32
                                    ).round(2)

def calculate_rolling_volatility(returns_df: pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame(mt.hv_composite(returns_df.values), 
                        index=returns_df.index,
                        columns=returns_df.columns
                        ).round(2)

def calculate_rolling_sharpe_ratio(returns_df: pd.DataFrame, length: int):
        
    return pd.DataFrame(mt.rolling_sharpe_ratios(
                        returns_df.values, 
                        length=length, 
                        min_length=length),
                        index=returns_df.index,
                        columns=returns_df.columns
                        ).round(2)

def calculate_rolling_drawdown(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:
    equity_curves = pd.DataFrame(equity_curves_calculs(returns_df.values),
                                index=returns_df.index,
                                columns=returns_df.columns,
                                dtype=np.float32
                                ).round(2)
    
    rolling_max = equity_curves.rolling(window=length, min_periods=1).max()
    drawdowns = (equity_curves - rolling_max) / rolling_max * Config.PERCENTAGE_FACTOR

    return drawdowns.round(2)

def calculate_rolling_average_correlation(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:
    correlation_matrices = returns_df.rolling(window=length, min_periods=length).corr()
    rolling_average_correlation = correlation_matrices.groupby(level=0).mean()

    return rolling_average_correlation.astype(np.float32).round(2)


def calculate_rolling_smoothed_skewness(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:

    rolling_mean = mt.rolling_mean(returns_df.values, length=20, min_length=20)

    return pd.DataFrame(mt.rolling_skewness(rolling_mean, length=length, min_length=length),
                        index=returns_df.index,
                        columns=returns_df.columns,
                        dtype=np.float32
                        ).round(2)