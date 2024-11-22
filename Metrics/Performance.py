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

    return rolling_mean(
        daily_returns, length=length, min_length=min_length) / rolling_volatility(
            daily_returns, length=length, min_length=min_length) * Config.ANNUALIZATION_FACTOR

def rolling_sortino_ratios(returns_array: np.ndarray, length: int, min_length: int) -> np.ndarray:
    
    # Calculer la moyenne mobile des rendements
    mean = rolling_mean(returns_array, length=length, min_length=min_length)
    
    # Calculer les rendements négatifs
    negative_returns = np.where(mean>=0, np.nan, mean)

    # Calculer l'écart-type mobile des rendements négatifs
    downside_std = rolling_volatility(negative_returns, length=length, min_length=min_length)
    
    return mean / downside_std * Config.ANNUALIZATION_FACTOR