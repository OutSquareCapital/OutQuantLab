from outquantlab.metrics.aggregation import (
    get_overall_mean,
    get_overall_min,
    get_rolling_max,
    get_rolling_mean,
)
from outquantlab.metrics.distribution import get_rolling_skewness
from outquantlab.metrics.maths_constants import ANNUALIZATION, PERCENTAGE, TimePeriod
from outquantlab.metrics.volatility import get_rolling_volatility, overall_volatility
from outquantlab.structures import arrays


def get_total_returns(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    equity_curves: arrays.ArrayFloat = arrays.get_prices_array(
        returns_array=returns_array
    )
    total_returns: arrays.ArrayFloat = equity_curves[-1]
    return total_returns - PERCENTAGE


def get_rolling_drawdown(
    returns_array: arrays.ArrayFloat, length: int
) -> arrays.ArrayFloat:
    equity_curves: arrays.ArrayFloat = arrays.get_prices_array(
        returns_array=returns_array
    )
    period_max: arrays.ArrayFloat = get_rolling_max(
        array=equity_curves, length=length, min_length=1
    )
    return (equity_curves - period_max) / period_max * PERCENTAGE


def get_max_drawdown(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    drawdown: arrays.ArrayFloat = get_rolling_drawdown(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return get_overall_min(array=drawdown)


def get_overall_average_drawdown(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    rolling_dd: arrays.ArrayFloat = get_rolling_drawdown(
        returns_array=returns_array,
        length=returns_array.shape[0],
    )

    return get_overall_mean(array=rolling_dd)


def expanding_sharpe_ratio(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    length: int = returns_array.shape[0]
    expanding_mean: arrays.ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=TimePeriod.HALF_YEAR
    )
    expanding_std: arrays.ArrayFloat = get_rolling_volatility(
        array=returns_array, length=length, min_length=TimePeriod.HALF_YEAR
    )
    return expanding_mean / expanding_std * ANNUALIZATION


def get_rolling_sharpe_ratio(
    returns_array: arrays.ArrayFloat, length: int
) -> arrays.ArrayFloat:
    mean: arrays.ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=length
    )
    volatility: arrays.ArrayFloat = get_rolling_volatility(
        array=returns_array, length=length, min_length=length
    )
    return mean / volatility * ANNUALIZATION


def get_overall_sharpe_ratio(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    mean: arrays.ArrayFloat = get_overall_mean(array=returns_array)
    volatility: arrays.ArrayFloat = overall_volatility(returns_array=returns_array)
    return mean / volatility * ANNUALIZATION


def get_overall_monthly_skewness(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    prices_array: arrays.ArrayFloat = arrays.get_prices_array(
        returns_array=returns_array
    )
    monthly_prices: arrays.ArrayFloat = arrays.reduce_array(
        array=prices_array, frequency=TimePeriod.MONTH
    )
    monthly_returns: arrays.ArrayFloat = arrays.pct_returns_array(
        prices_array=monthly_prices
    )
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: arrays.ArrayFloat = get_rolling_skewness(
        array=monthly_returns, length=length_to_use, min_length=4
    )
    return get_overall_mean(array=expanding_skew)


def get_returns_distribution(
    returns_array: arrays.ArrayFloat, frequency: int
) -> arrays.ArrayFloat:
    resampled_returns: arrays.ArrayFloat = arrays.reduce_array(
        array=returns_array, frequency=frequency
    )
    return resampled_returns * PERCENTAGE
