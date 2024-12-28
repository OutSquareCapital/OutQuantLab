import numpy as np
from scipy.stats import skew # type: ignore
from Utilitary import PERCENTAGE_FACTOR, DataFrameFloat, SeriesFloat, Float32
from Indicators import calculate_equity_curves
from Metrics import rolling_mean, rolling_sharpe_ratios, rolling_skewness, hv_composite, overall_volatility
from Metrics.Performance import overall_sharpe_ratio

def calculate_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.nparray),
        index=returns_df.index,
        columns=returns_df.columns
        )
    
    return SeriesFloat((
        equity_curves.iloc[-1]-100), # type: ignore
        index=returns_df.columns)

def calculate_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat|Float32:

    overall_vol = overall_volatility(returns_df.nparray)

    return SeriesFloat(
        data=overall_vol, 
        index=returns_df.columns
        )

def calculate_overall_sharpe_ratio(returns_df: DataFrameFloat | SeriesFloat) -> SeriesFloat:
    sharpes = overall_sharpe_ratio(returns_df.nparray)
    
    return SeriesFloat(sharpes, index=returns_df.columns)

def calculate_overall_average_drawdown(returns_df: DataFrameFloat, length: int) -> SeriesFloat:

    return calculate_rolling_drawdown(returns_df, length).mean()

def calculate_overall_max_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:

    return calculate_ath_drawdown(returns_df).mean()

def calculate_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:

    def calculate_skew(series: SeriesFloat):
        return skew(series, nan_policy='omit')

    monthly_returns_df = returns_df.resample('ME').mean()
    
    return monthly_returns_df.apply(
        calculate_skew
        ).astype(Float32
        )

def calculate_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:

    return returns_df.corr().mean()

def calculate_equity_curves_df(returns_df: DataFrameFloat) -> DataFrameFloat:

    
    return DataFrameFloat(
        calculate_equity_curves(returns_df.nparray),
        index=returns_df.index,
        columns=returns_df.columns
        )

def format_returns(returns_df: DataFrameFloat, limit: float) -> DataFrameFloat:
    lower_threshold = returns_df.quantile(limit, axis=0) 
    upper_threshold = returns_df.quantile(1-limit, axis=0) 
    
    formatted_returns_df = returns_df.where((returns_df >= lower_threshold) & (returns_df <= upper_threshold), np.nan) 
    formatted_returns_df = formatted_returns_df * PERCENTAGE_FACTOR

    return DataFrameFloat(formatted_returns_df)

def calculate_rolling_volatility(returns_df: DataFrameFloat) -> DataFrameFloat:

    return DataFrameFloat(
        hv_composite(returns_df.nparray),
        index=returns_df.index,
        columns=returns_df.columns
        )

def calculate_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:

    return DataFrameFloat(
        rolling_sharpe_ratios(
        returns_df.nparray,
        length=length, 
        min_length=length),
        index=returns_df.index,
        columns=returns_df.columns
        )

def calculate_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.nparray), 
        index=returns_df.index, 
        columns=returns_df.columns
        )
    
    rolling_max = equity_curves.rolling(window=length, min_periods=1).max()

    return (equity_curves - rolling_max) / rolling_max * PERCENTAGE_FACTOR

def calculate_ath_drawdown(returns_df: DataFrameFloat) -> DataFrameFloat:
    
    equity_curves = DataFrameFloat(
        calculate_equity_curves(returns_df.nparray), 
        index=returns_df.index, 
        columns=returns_df.columns
        )
    
    equity_max = equity_curves.max(axis=0) 
    drawdowns = (equity_curves - equity_max) / equity_max * PERCENTAGE_FACTOR

    return drawdowns

def calculate_rolling_average_correlation(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    rolling_avg_corr = returns_df.rolling( 
        window=length, 
        min_periods=length
    ).corr( # type: ignore
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
        index=returns_df.index, 
        columns=returns_df.columns
        )