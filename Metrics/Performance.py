import numpy as np
import Config
from .Aggregation import rolling_mean
from .Volatility import rolling_volatility

def expanding_sharpe_ratios(daily_returns: np.ndarray) -> np.ndarray:

    length = daily_returns.shape[0]

    expanding_mean = rolling_mean(daily_returns, length=length, min_length=125)
    expanding_std = rolling_volatility(daily_returns, length=length, min_length=125) 
    
    return expanding_mean/expanding_std * Config.ANNUALIZATION_FACTOR


def rolling_sharpe_ratios(daily_returns: np.ndarray, length:int, min_length:int) -> np.ndarray:

    mean = rolling_mean(daily_returns, length=length, min_length=min_length)

    volatility = rolling_volatility(daily_returns, length=length, min_length=min_length)
    return  mean / volatility * Config.ANNUALIZATION_FACTOR