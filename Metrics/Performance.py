import numpy as np
from Files import ANNUALIZATION_FACTOR
from .Aggregation import rolling_mean
from .Volatility import rolling_volatility

def expanding_sharpe_ratios(returns_array: np.ndarray) -> np.ndarray:

    length = returns_array.shape[0]

    expanding_mean = rolling_mean(returns_array, length=length, min_length=125)
    expanding_std = rolling_volatility(returns_array, length=length, min_length=125) 
    
    return expanding_mean/expanding_std * ANNUALIZATION_FACTOR


def rolling_sharpe_ratios(returns_array: np.ndarray, length:int, min_length:int) -> np.ndarray:

    mean = rolling_mean(returns_array, length=length, min_length=min_length)

    volatility = rolling_volatility(returns_array, length=length, min_length=min_length)
    return  mean / volatility * ANNUALIZATION_FACTOR