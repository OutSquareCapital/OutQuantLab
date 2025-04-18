from numquant.arrays.extract import get_pct_returns, get_prices
from numquant.arrays.transform import reduce
from numquant.main import Float2D
from numquant.metrics.constants import ANNUALIZATION, PERCENTAGE, Period
from numquant.metrics.rolling.main import get_expanding_mean, get_max, get_mean
from numquant.metrics.rolling.volatility import get_expanding_volatility, get_volatility


def get_sharpe_ratio(returns_array: Float2D, length: int) -> Float2D:
    mean: Float2D = get_mean(array=returns_array, length=length, min_length=length)
    volatility: Float2D = get_volatility(
        array=returns_array, length=length, min_length=length
    )
    return mean / volatility * ANNUALIZATION


def expanding_sharpe_ratio(returns_array: Float2D) -> Float2D:
    expanding_mean: Float2D = get_expanding_mean(
        array=returns_array, min_length=Period.HALF_YEAR
    )
    expanding_std: Float2D = get_expanding_volatility(
        array=returns_array, min_length=Period.HALF_YEAR
    )
    return expanding_mean / expanding_std * ANNUALIZATION


def get_rolling_drawdown(returns_array: Float2D, length: int) -> Float2D:
    equity_curves: Float2D = get_prices(returns=returns_array)
    period_max: Float2D = get_max(array=equity_curves, length=length, min_length=1)
    return (equity_curves - period_max) / period_max * PERCENTAGE


def get_equity(returns_array: Float2D, frequency: int | None = None) -> Float2D:
    equity: Float2D = get_prices(returns=returns_array)
    if frequency is None:
        return equity
    return reduce(array=equity, frequency=frequency)


def get_returns_distribution(returns_array: Float2D, frequency: int | None = None) -> Float2D:
    equity: Float2D = get_equity(
        returns_array=returns_array, frequency=frequency
    )
    return get_pct_returns(prices=equity) * PERCENTAGE
