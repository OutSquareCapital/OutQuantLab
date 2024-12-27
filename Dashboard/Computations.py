import pandas as pd
import numpy as np
from scipy.stats import skew # type: ignore
from Files import PERCENTAGE_FACTOR, ANNUALIZATION_FACTOR, ANNUALIZED_PERCENTAGE_FACTOR
from Indicators import calculate_equity_curves
from Metrics import rolling_mean, rolling_sharpe_ratios, rolling_skewness, hv_composite

def calculate_overall_returns(returns_df: pd.DataFrame) -> pd.Series:
    
    equity_curves = pd.DataFrame(
        calculate_equity_curves(returns_df.values), # type: ignore
        index=returns_df.index, # type: ignore
        columns=returns_df.columns,
        dtype=np.float32
        )

    return pd.Series(
        (
        equity_curves.iloc[-1]-100),
        index=returns_df.columns,
        dtype=np.float32
        ).round(2) # type: ignore

def calculate_overall_volatility(returns_df: pd.DataFrame) -> pd.Series:

    return (returns_df.std() * ANNUALIZED_PERCENTAGE_FACTOR).round(2) # type: ignore

def calculate_overall_sharpe_ratio(returns_df: pd.DataFrame) -> pd.Series:

    return (
        (returns_df.mean() / returns_df.std() # type: ignore
        ) * ANNUALIZATION_FACTOR
        ).round(2)

def calculate_overall_average_drawdown(returns_df: pd.DataFrame, length: int) -> pd.Series:

    return calculate_rolling_drawdown(returns_df, length).mean().round(2) # type: ignore

def calculate_overall_max_drawdown(returns_df: pd.DataFrame) -> pd.Series:

    return calculate_ath_drawdown(returns_df).mean().round(2) # type: ignore


def calculate_overall_monthly_skew(returns_df: pd.DataFrame) -> pd.Series:

    monthly_returns_df = returns_df.resample('ME').mean() # type: ignore
    
    return monthly_returns_df.apply(
        lambda x: skew(x, nan_policy='omit') # type: ignore
        ).astype(np.float32
        ).round(2) # type: ignore

def calculate_overall_average_correlation(returns_df: pd.DataFrame) -> pd.Series:

    return returns_df.corr().mean().round(2) # type: ignore

def calculate_equity_curves_df(returns_df: pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame(
        calculate_equity_curves(returns_df.values),  # type: ignore
        index=returns_df.index,  # type: ignore
        columns=returns_df.columns,
        dtype=np.float32
        ).round(2)

def format_returns(returns_df: pd.DataFrame, limit: float) -> pd.DataFrame:
    lower_threshold = returns_df.quantile(limit, axis=0) # type: ignore
    upper_threshold = returns_df.quantile(1-limit, axis=0) # type: ignore
    
    formatted_returns_df = returns_df.where((returns_df >= lower_threshold) & (returns_df <= upper_threshold), np.nan) # type: ignore
    formatted_returns_df = formatted_returns_df * PERCENTAGE_FACTOR

    return formatted_returns_df.round(2) # type: ignore

def calculate_rolling_volatility(returns_df: pd.DataFrame) -> pd.DataFrame:

    return pd.DataFrame(
        hv_composite(returns_df.values),  # type: ignore
        index=returns_df.index, # type: ignore
        columns=returns_df.columns
        ).round(2)

def calculate_rolling_sharpe_ratio(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:

    return pd.DataFrame(
        rolling_sharpe_ratios(
        returns_df.values,  # type: ignore
        length=length, 
        min_length=length),
        index=returns_df.index, # type: ignore
        columns=returns_df.columns
        ).round(2) # type: ignore

def calculate_rolling_drawdown(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:
    
    equity_curves = pd.DataFrame(
        calculate_equity_curves(returns_df.values), # type: ignore
        index=returns_df.index, # type: ignore
        columns=returns_df.columns,
        dtype=np.float32
        ).round(2)
    
    rolling_max = equity_curves.rolling(window=length, min_periods=1).max()
    drawdowns = (equity_curves - rolling_max) / rolling_max * PERCENTAGE_FACTOR

    return drawdowns.round(2) # type: ignore


def calculate_ath_drawdown(returns_df: pd.DataFrame) -> pd.DataFrame:
    
    equity_curves = pd.DataFrame(
        calculate_equity_curves(returns_df.values), # type: ignore
        index=returns_df.index, # type: ignore
        columns=returns_df.columns,
        dtype=np.float32
        ).round(2)
    
    equity_max = equity_curves.max(axis=0) # type: ignore
    drawdowns = (equity_curves - equity_max) / equity_max * PERCENTAGE_FACTOR

    return drawdowns.round(2) # type: ignore

def calculate_rolling_average_correlation(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:

    return returns_df.rolling( # type: ignore
        window=length, min_periods=length
        ).corr(
        ).groupby(level=0
        ).mean(
        ).astype(np.float32
        ).round(2)


def calculate_correlation_matrix(returns_df: pd.DataFrame) -> pd.DataFrame:

    return returns_df.corr().round(2) # type: ignore

def calculate_rolling_smoothed_skewness(returns_df: pd.DataFrame, length: int) -> pd.DataFrame:

    smoothed_returns = rolling_mean(returns_df.values, length=20, min_length=20) # type: ignore

    skewness_array = rolling_skewness(array=smoothed_returns, length=length, min_length=length)

    return pd.DataFrame( # type: ignore
        data=skewness_array,
        index=returns_df.index, # type: ignore
        columns=returns_df.columns,
        dtype=np.float32
        ).round(2)