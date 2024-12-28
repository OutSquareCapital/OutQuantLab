from Files import ArrayFloat
from Files import ANNUALIZATION_FACTOR
from .Aggregation import rolling_mean, overall_mean
from .Volatility import rolling_volatility, overall_volatility

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

    mean = overall_mean(returns_array)
    volatility = overall_volatility(returns_array)

    return mean / volatility * ANNUALIZATION_FACTOR