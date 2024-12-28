import numpy as np
from scipy.stats import skew # type: ignore
from Files import PERCENTAGE_FACTOR, ANNUALIZATION_FACTOR, DataFrameFloat, SeriesFloat
from Indicators import calculate_equity_curves
from Metrics import rolling_mean, rolling_sharpe_ratios, rolling_skewness, hv_composite, overall_volatility

def calculate_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.values),
        index=returns_df.index,
        columns=returns_df.columns
        )
    
    return SeriesFloat((
        equity_curves.iloc[-1]-100), # type: ignore
        index=returns_df.columns
        ).round(2)# type: ignore

def calculate_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat:

    overall_vol = overall_volatility(returns_df.values)
    return SeriesFloat(
        data=overall_vol, 
        index=returns_df.columns
        ).round(2) # type: ignore

def calculate_overall_sharpe_ratio(returns_df: DataFrameFloat) -> SeriesFloat:

    return ((
        returns_df.mean() / returns_df.std() # type: ignore
        ) * ANNUALIZATION_FACTOR
        ).round(2) # type: ignore

def calculate_overall_average_drawdown(returns_df: DataFrameFloat, length: int) -> SeriesFloat:

    return calculate_rolling_drawdown(returns_df, length).mean().round(2) 

def calculate_overall_max_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:

    return calculate_ath_drawdown(returns_df).mean().round(2) 

def calculate_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:

    monthly_returns_df = returns_df.resample('ME').mean() 
    
    return monthly_returns_df.apply(
        lambda x: skew(x, nan_policy='omit') 
        ).astype(np.float32
        ).round(2) # type: ignore

def calculate_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:

    return returns_df.corr().mean().round(2)

def calculate_equity_curves_df(returns_df: DataFrameFloat) -> DataFrameFloat:

    
    return DataFrameFloat(
        calculate_equity_curves(returns_df.values),
        index=returns_df.index,
        columns=returns_df.columns
        ).round(2)

def format_returns(returns_df: DataFrameFloat, limit: float) -> DataFrameFloat:
    lower_threshold = returns_df.quantile(limit, axis=0) 
    upper_threshold = returns_df.quantile(1-limit, axis=0) 
    
    formatted_returns_df = returns_df.where((returns_df >= lower_threshold) & (returns_df <= upper_threshold), np.nan) 
    formatted_returns_df = formatted_returns_df * PERCENTAGE_FACTOR

    return DataFrameFloat(formatted_returns_df.round(2))

def calculate_rolling_volatility(returns_df: DataFrameFloat) -> DataFrameFloat:

    return DataFrameFloat(
        hv_composite(returns_df.values),
        index=returns_df.index,
        columns=returns_df.columns
        ).round(2)

def calculate_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:

    return DataFrameFloat(
        rolling_sharpe_ratios(
        returns_df.values,
        length=length, 
        min_length=length),
        index=returns_df.index,
        columns=returns_df.columns
        ).round(2)

def calculate_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.values), 
        index=returns_df.index, 
        columns=returns_df.columns
        ).round(2)
    
    rolling_max = equity_curves.rolling(window=length, min_periods=1).max()
    drawdowns = (equity_curves - rolling_max) / rolling_max * PERCENTAGE_FACTOR

    return drawdowns.round(2) 

def calculate_ath_drawdown(returns_df: DataFrameFloat) -> DataFrameFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.values), 
        index=returns_df.index, 
        columns=returns_df.columns
        ).round(2)
    
    equity_max = equity_curves.max(axis=0) 
    drawdowns = (equity_curves - equity_max) / equity_max * PERCENTAGE_FACTOR

    return drawdowns.round(2) 

def calculate_rolling_average_correlation(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    rolling_avg_corr = returns_df.rolling( 
        window=length, 
        min_periods=length
    ).corr( # type: ignore
    ).groupby(level=0
    ).mean(
    ).astype(np.float32
    ).round(2) # type: ignore

    return DataFrameFloat(rolling_avg_corr)

def calculate_correlation_matrix(returns_df: DataFrameFloat) -> DataFrameFloat:

    return DataFrameFloat(returns_df.corr()).round(2) 

def calculate_rolling_smoothed_skewness(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:

    smoothed_returns = rolling_mean(returns_df.values, length=20, min_length=20) 

    skewness_array = rolling_skewness(array=smoothed_returns, length=length, min_length=length)

    return DataFrameFloat( 
        data=skewness_array,
        index=returns_df.index, 
        columns=returns_df.columns
        ).round(2)