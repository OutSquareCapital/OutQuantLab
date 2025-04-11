from numquant.metrics.aggregate import get_mean, get_min, get_volatility
from numquant.main import Float2D
from numquant.constants import MONTH, PERCENTAGE, ANNUALIZATION
from numquant.metrics.rolling import get_rolling_drawdown, get_skewness
from numquant.arrays import get_prices, reduce, get_pct_returns

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
    equity_curves: Float2D = get_prices(
        returns=returns_array
    )
    total_returns: Float2D = equity_curves[-1]
    return total_returns - PERCENTAGE

def get_monthly_skewness(returns_array: Float2D) -> Float2D:
    prices_array: Float2D = get_prices(
        returns=returns_array
    )
    monthly_prices: Float2D = reduce(
        array=prices_array, frequency=MONTH
    )
    monthly_returns: Float2D = get_pct_returns(
        prices=monthly_prices
    )
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: Float2D = get_skewness(
        array=monthly_returns, length=length_to_use, min_length=4
    )
    return get_mean(array=expanding_skew)