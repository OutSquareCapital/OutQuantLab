from outquantlab.metrics.aggregation import (
    get_overall_mean,
    get_overall_min,
    get_rolling_max,
    get_rolling_mean,
)
from outquantlab.metrics.distribution import get_rolling_skewness
from outquantlab.metrics.volatility import get_rolling_volatility, overall_volatility
from outquantlab.structures import arrays, consts


def get_total_returns(returns_array: arrays.Float2D) -> arrays.Float2D:
    equity_curves: arrays.Float2D = arrays.get_prices_array(
        returns_array=returns_array
    )
    total_returns: arrays.Float2D = equity_curves[-1]
    return total_returns - consts.PERCENTAGE


def get_rolling_drawdown(
    returns_array: arrays.Float2D, length: int
) -> arrays.Float2D:
    equity_curves: arrays.Float2D = arrays.get_prices_array(
        returns_array=returns_array
    )
    period_max: arrays.Float2D = get_rolling_max(
        array=equity_curves, length=length, min_length=1
    )
    return (equity_curves - period_max) / period_max * consts.PERCENTAGE


def get_max_drawdown(returns_array: arrays.Float2D) -> arrays.Float2D:
    drawdown: arrays.Float2D = get_rolling_drawdown(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return get_overall_min(array=drawdown)


def get_overall_average_drawdown(returns_array: arrays.Float2D) -> arrays.Float2D:
    rolling_dd: arrays.Float2D = get_rolling_drawdown(
        returns_array=returns_array,
        length=returns_array.shape[0],
    )

    return get_overall_mean(array=rolling_dd)


def expanding_sharpe_ratio(returns_array: arrays.Float2D) -> arrays.Float2D:
    length: int = returns_array.shape[0]
    expanding_mean: arrays.Float2D = get_rolling_mean(
        array=returns_array, length=length, min_length=consts.HALF_YEAR
    )
    expanding_std: arrays.Float2D = get_rolling_volatility(
        array=returns_array, length=length, min_length=consts.HALF_YEAR
    )
    return expanding_mean / expanding_std * consts.ANNUALIZATION


def get_rolling_sharpe_ratio(
    returns_array: arrays.Float2D, length: int
) -> arrays.Float2D:
    mean: arrays.Float2D = get_rolling_mean(
        array=returns_array, length=length, min_length=length
    )
    volatility: arrays.Float2D = get_rolling_volatility(
        array=returns_array, length=length, min_length=length
    )
    return mean / volatility * consts.ANNUALIZATION


def get_overall_sharpe_ratio(returns_array: arrays.Float2D) -> arrays.Float2D:
    mean: arrays.Float2D = get_overall_mean(array=returns_array)
    volatility: arrays.Float2D = overall_volatility(returns_array=returns_array)
    return mean / volatility * consts.ANNUALIZATION


def get_overall_monthly_skewness(returns_array: arrays.Float2D) -> arrays.Float2D:
    prices_array: arrays.Float2D = arrays.get_prices_array(
        returns_array=returns_array
    )
    monthly_prices: arrays.Float2D = arrays.reduce_array(
        array=prices_array, frequency=consts.MONTH
    )
    monthly_returns: arrays.Float2D = arrays.pct_returns_array(
        prices_array=monthly_prices
    )
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: arrays.Float2D = get_rolling_skewness(
        array=monthly_returns, length=length_to_use, min_length=4
    )
    return get_overall_mean(array=expanding_skew)


def get_returns_distribution(
    returns_array: arrays.Float2D, frequency: int
) -> arrays.Float2D:
    resampled_returns: arrays.Float2D = arrays.reduce_array(
        array=returns_array, frequency=frequency
    )
    return resampled_returns * consts.PERCENTAGE
