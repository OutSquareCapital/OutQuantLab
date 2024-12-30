from Metrics import calculate_overall_min
from Utilitary import ANNUALIZATION_FACTOR, PERCENTAGE_FACTOR, ArrayFloat, ArrayInt
from Metrics.Aggregation import rolling_mean, calculate_overall_mean, rolling_max, calculate_overall_max, calculate_overall_min
from Metrics.Volatility import rolling_volatility, overall_volatility
from Metrics.Distribution import rolling_skewness
import numpy as np

def reduce_array(prices_array: ArrayFloat, frequency: int) -> ArrayFloat:
    array_length: int = prices_array.shape[0]
    indices: ArrayInt = np.arange(
        start=0,
        stop=array_length, 
        step=frequency)

    if array_length % frequency != 0:
        indices: ArrayInt = np.append(arr=indices, values=array_length - 1)
    return prices_array[indices]

def shift_array(returns_array: ArrayFloat, step:int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = np.empty_like(prototype=returns_array)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array

def calculate_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, 
    hv_array: ArrayFloat, 
    target_volatility: int = 15
    ) -> ArrayFloat:
    vol_adj_position_size_shifted: ArrayFloat = shift_array(returns_array=target_volatility / hv_array)
    return pct_returns_array * vol_adj_position_size_shifted

def calculate_equity_curves(returns_array: ArrayFloat) -> ArrayFloat:
    temp_array:ArrayFloat = returns_array.copy()
    mask: ArrayFloat = np.isnan(temp_array)
    temp_array[mask] = 0
    cumulative_returns: ArrayFloat = np.cumprod(a=1 + temp_array, axis=0)
    cumulative_returns[mask] = np.nan

    return cumulative_returns * PERCENTAGE_FACTOR

def log_returns_np(prices_array: ArrayFloat) -> ArrayFloat:
    ratios = prices_array[1:] / prices_array[:-1]
    log_returns_array: ArrayFloat = np.empty_like(prototype=prices_array)
    log_returns_array[0] = np.nan
    log_returns_array[1:] = np.log(ratios)
    return log_returns_array

def pct_returns_np(prices_array: ArrayFloat) -> ArrayFloat:
    pct_returns_array: ArrayFloat = np.empty_like(prototype=prices_array)
    pct_returns_array[0] = np.nan
    pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    return pct_returns_array

def calculate_total_returns(returns_array: ArrayFloat) -> ArrayFloat:
    equity_curves: ArrayFloat = calculate_equity_curves(returns_array=returns_array)
    return equity_curves[-1] - 100

def calculate_rolling_drawdown(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    equity_curves: ArrayFloat = calculate_equity_curves(returns_array=returns_array)
    period_max: ArrayFloat = rolling_max(array=equity_curves, length=length, min_length=1)
    return (equity_curves - period_max) / period_max * PERCENTAGE_FACTOR

def calculate_ath_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    equity_curves: ArrayFloat = calculate_equity_curves(returns_array=returns_array)
    equity_max: ArrayFloat = calculate_overall_max(array=equity_curves)
    return (equity_curves - equity_max) / equity_max * PERCENTAGE_FACTOR

def calculate_max_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    drawdown: ArrayFloat = calculate_ath_drawdown(returns_array=returns_array)
    return calculate_overall_min(array=drawdown)

def expanding_sharpe_ratios(returns_array: ArrayFloat) -> ArrayFloat:
    length: int = returns_array.shape[0]
    expanding_mean: ArrayFloat = rolling_mean(returns_array, length=length, min_length=125)
    expanding_std: ArrayFloat = rolling_volatility(returns_array, length=length, min_length=125) 
    return expanding_mean/expanding_std * ANNUALIZATION_FACTOR

def rolling_sharpe_ratios(returns_array: ArrayFloat, length:int, min_length:int) -> ArrayFloat:
    mean: ArrayFloat = rolling_mean(array=returns_array, length=length, min_length=min_length)
    volatility: ArrayFloat = rolling_volatility(array=returns_array, length=length, min_length=min_length)
    return  mean / volatility * ANNUALIZATION_FACTOR

def overall_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:
    mean: ArrayFloat = calculate_overall_mean(array=returns_array)
    volatility: ArrayFloat = overall_volatility(array=returns_array)
    return mean / volatility * ANNUALIZATION_FACTOR

def calculate_overall_monthly_skewness(returns_array: ArrayFloat) -> ArrayFloat:
    prices_array: ArrayFloat = calculate_equity_curves(returns_array=returns_array)
    monthly_prices: ArrayFloat = reduce_array(prices_array=prices_array, frequency=21)
    monthly_returns: ArrayFloat = pct_returns_np(prices_array=monthly_prices)
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: ArrayFloat = rolling_skewness(array=monthly_returns, length=length_to_use, min_length=4)
    return calculate_overall_mean(array=expanding_skew)
