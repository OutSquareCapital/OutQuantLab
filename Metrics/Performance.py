from Utilitary import ANNUALIZATION_FACTOR, PERCENTAGE_FACTOR, ArrayFloat, Float32
from .Aggregation import rolling_mean, calculate_overall_mean, rolling_max, calculate_overall_max
from .Volatility import rolling_volatility, overall_volatility
import numpy as np

def shift_array(returns_array: ArrayFloat, step:int = 1) -> ArrayFloat:
    shifted_array = np.empty_like(returns_array, dtype=Float32)
    shifted_array[step:, :] = returns_array[:-step, :]
    shifted_array[:step, :] = np.nan
    return shifted_array

def calculate_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, 
    hv_array: ArrayFloat, 
    target_volatility: int = 15
    ) -> ArrayFloat:

    vol_adj_position_size_shifted:ArrayFloat = shift_array(target_volatility / hv_array)

    return pct_returns_array * vol_adj_position_size_shifted

def calculate_equity_curves(returns_array: ArrayFloat) -> ArrayFloat:

    temp_array:ArrayFloat = returns_array.copy()
    mask = np.isnan(temp_array)
    temp_array[mask] = 0
    cumulative_returns = np.cumprod(1 + temp_array, axis=0)
    cumulative_returns[mask] = np.nan

    return cumulative_returns * PERCENTAGE_FACTOR

def log_returns_np(prices_array: ArrayFloat) -> ArrayFloat:

    if prices_array.ndim == 1:
        log_returns_array = np.empty(prices_array.shape, dtype=Float32)
        log_returns_array[0] = np.nan
        log_returns_array[1:] = np.log(prices_array[1:] / prices_array[:-1])
    else:
        log_returns_array = np.empty(prices_array.shape, dtype=Float32)
        log_returns_array[0, :] = np.nan
        log_returns_array[1:, :] = np.log(prices_array[1:] / prices_array[:-1])

    return log_returns_array

def pct_returns_np(prices_array: ArrayFloat) -> ArrayFloat:

    if prices_array.ndim == 1:
        pct_returns_array = np.empty(prices_array.shape, dtype=Float32)
        pct_returns_array[0] = np.nan
        pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    else:
        pct_returns_array = np.empty(prices_array.shape, dtype=Float32)
        pct_returns_array[0, :] = np.nan
        pct_returns_array[1:, :] = prices_array[1:] / prices_array[:-1] - 1

    return pct_returns_array

def calculate_rolling_drawdown(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    
    equity_curves = calculate_equity_curves(returns_array)
    
    period_max = rolling_max(equity_curves, length=length, min_length=1)

    return (equity_curves - period_max) / period_max * PERCENTAGE_FACTOR

def calculate_ath_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    
    equity_curves = calculate_equity_curves(returns_array)

    equity_max = calculate_overall_max(equity_curves)

    return (equity_curves - equity_max) / equity_max * PERCENTAGE_FACTOR

def calculate_max_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    
    drawdown = calculate_ath_drawdown(returns_array)
    
    return calculate_overall_max(drawdown)

def expanding_sharpe_ratios(returns_array: ArrayFloat) -> ArrayFloat:

    length = returns_array.shape[0]

    expanding_mean = rolling_mean(returns_array, length=length, min_length=125)
    expanding_std = rolling_volatility(returns_array, length=length, min_length=125) 
    
    return expanding_mean/expanding_std * ANNUALIZATION_FACTOR


def rolling_sharpe_ratios(returns_array: ArrayFloat, length:int, min_length:int) -> ArrayFloat:

    mean = rolling_mean(returns_array, length=length, min_length=min_length)

    volatility = rolling_volatility(returns_array, length=length, min_length=min_length)
    return  mean / volatility * ANNUALIZATION_FACTOR

def overall_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:

    mean = calculate_overall_mean(returns_array)
    volatility = overall_volatility(returns_array)

    return mean / volatility * ANNUALIZATION_FACTOR