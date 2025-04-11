from numquant.arrays import get_pct_returns, get_prices, reduce
from numquant.main import Float2D
from numquant.metrics.aggregate.main import get_mean, get_min
from numquant.metrics.aggregate.volatility import get_volatility
from numquant.metrics.constants import ANNUALIZATION, PERCENTAGE, Period
from numquant.metrics.rolling import get_expanding_skewness, get_rolling_drawdown


def get_sharpe_ratio(returns_array: Float2D) -> Float2D:
    mean: Float2D = get_mean(array=returns_array)
    volatility: Float2D = get_volatility(returns_array=returns_array)
    return mean / volatility * ANNUALIZATION


def get_average_drawdown(returns_array: Float2D) -> Float2D:
    rolling_dd: Float2D = get_rolling_drawdown(
        returns_array=returns_array,
        length=returns_array.shape[0],
    )

    return get_mean(array=rolling_dd)


def get_max_drawdown(returns_array: Float2D) -> Float2D:
    drawdown: Float2D = get_rolling_drawdown(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return get_min(array=drawdown)


def get_total_returns(returns_array: Float2D) -> Float2D:
    equity_curves: Float2D = get_prices(returns=returns_array)
    total_returns: Float2D = equity_curves[-1]
    return total_returns - PERCENTAGE


def get_monthly_skewness(returns_array: Float2D) -> Float2D:
    prices_array: Float2D = get_prices(returns=returns_array)
    monthly_prices: Float2D = reduce(array=prices_array, frequency=Period.MONTH)
    monthly_returns: Float2D = get_pct_returns(prices=monthly_prices)
    expanding_skew: Float2D = get_expanding_skewness(array=monthly_returns)
    return get_mean(array=expanding_skew)
