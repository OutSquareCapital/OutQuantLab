import numpy as np
from Utilitary import PERCENTAGE_FACTOR, ArrayFloat, DataFrameFloat, SeriesFloat, Float32
from Metrics import (
    rolling_mean, 
    rolling_sharpe_ratios, 
    rolling_skewness, 
    hv_composite, 
    overall_volatility, 
    calculate_equity_curves, 
    calculate_overall_mean, 
    overall_sharpe_ratio, 
    calculate_max_drawdown, 
    calculate_rolling_drawdown,
    )

def calculate_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.nparray),
        index=returns_df.dates,
        columns=returns_df.columns
        )
    
    return SeriesFloat((
        equity_curves.iloc[-1]-100),
        index=returns_df.columns)

def calculate_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat:

    overall_vol = overall_volatility(returns_df.nparray)

    return SeriesFloat(data=overall_vol, index=returns_df.columns)

def calculate_overall_sharpe_ratio(returns_df: DataFrameFloat) -> SeriesFloat:

    sharpes = overall_sharpe_ratio(returns_df.nparray)
    
    return SeriesFloat(sharpes, index=returns_df.columns)

def calculate_overall_average_drawdown(returns_df: DataFrameFloat, length: int) -> SeriesFloat:
    
    rolling_dd = calculate_rolling_drawdown(returns_df.nparray, length)

    mean_rolling_dd = calculate_overall_mean(rolling_dd)

    return SeriesFloat(mean_rolling_dd, index=returns_df.columns)

def calculate_overall_max_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:

    return SeriesFloat(calculate_max_drawdown(returns_df.nparray), returns_df.columns)

def calculate_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:

    monthly_returns_df= returns_df.resample('ME').mean()
    print(f'Monthly Returns: {monthly_returns_df}')
    length_to_use = len(monthly_returns_df)
    print(f'Length to use: {length_to_use}')
    montly_returns_array: ArrayFloat = monthly_returns_df.to_numpy()
    print(f'Monthly Returns Array: {montly_returns_array}')
    overall_skew = rolling_skewness(montly_returns_array, length=length_to_use, min_length=4)
    print(f'Overall Skew: {overall_skew}')
    average_overall_skew = calculate_overall_mean(overall_skew)
    return SeriesFloat(average_overall_skew, index=returns_df.columns)

def calculate_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:
    
    return SeriesFloat(returns_df.corr().mean(), index=returns_df.columns)

def format_returns(returns_df: DataFrameFloat, limit: float) -> DataFrameFloat:
    lower_threshold = SeriesFloat(returns_df.quantile(limit, axis=0) ) 
    upper_threshold = SeriesFloat(returns_df.quantile(1-limit, axis=0) )
    
    formatted_returns_df = DataFrameFloat(returns_df.where((returns_df >= lower_threshold) & (returns_df <= upper_threshold), np.nan))

    return formatted_returns_df * PERCENTAGE_FACTOR

def calculate_rolling_volatility(returns_df: DataFrameFloat) -> DataFrameFloat:

    return DataFrameFloat(
        hv_composite(returns_df.nparray),
        index=returns_df.dates,
        columns=returns_df.columns
        )

def calculate_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:

    return DataFrameFloat(
        rolling_sharpe_ratios(
        returns_df.nparray,
        length=length, 
        min_length=length),
        index=returns_df.dates,
        columns=returns_df.columns
        )

def calculate_rolling_average_correlation(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    rolling_avg_corr = returns_df.rolling( 
        window=length, 
        min_periods=length
    ).corr(
    ).groupby(level=0
    ).mean(
    ).astype(Float32
    )

    return DataFrameFloat(rolling_avg_corr)

def calculate_correlation_matrix(returns_df: DataFrameFloat) -> DataFrameFloat:

    return DataFrameFloat(returns_df.corr())

def calculate_rolling_smoothed_skewness(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:

    smoothed_returns = rolling_mean(returns_df.nparray, length=20, min_length=20) 

    skewness_array = rolling_skewness(array=smoothed_returns, length=length, min_length=length)

    return DataFrameFloat( 
        data=skewness_array,
        index=returns_df.dates, 
        columns=returns_df.columns
        )