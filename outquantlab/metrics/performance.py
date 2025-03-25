from outquantlab.typing_conventions import ArrayFloat, ArrayInt
from outquantlab.metrics.maths_constants import Standardization, TimePeriod
from outquantlab.metrics.aggregation import (
    get_rolling_mean,
    get_overall_mean,
    get_rolling_max,
    get_overall_min,
)
from outquantlab.metrics.volatility import get_rolling_volatility, overall_volatility
from outquantlab.metrics.distribution import get_rolling_skewness
from numpy import log, nan, cumprod, arange, append, empty_like, isnan


def reduce_array(prices_array: ArrayFloat, frequency: int) -> ArrayFloat:
    array_length: int = prices_array.shape[0]
    indices: ArrayInt = arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        indices: ArrayInt = append(arr=indices, values=array_length - 1)
    return prices_array[indices]


def get_equity_curves(returns_array: ArrayFloat) -> ArrayFloat:
    temp_array: ArrayFloat = returns_array.copy()
    mask: ArrayFloat = isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns: ArrayFloat = empty_like(prototype=temp_array)

    cumulative_returns[:0] = nan

    cumulative_returns[0:] = cumprod(a=1 + temp_array[0:], axis=0)

    cumulative_returns[mask] = nan

    return cumulative_returns * Standardization.PERCENTAGE.value


def log_returns_np(prices_array: ArrayFloat) -> ArrayFloat:
    ratios = prices_array[1:] / prices_array[:-1]
    log_returns_array: ArrayFloat = empty_like(prototype=prices_array)
    log_returns_array[0] = nan
    log_returns_array[1:] = log(ratios)
    return log_returns_array


def pct_returns_np(prices_array: ArrayFloat) -> ArrayFloat:
    pct_returns_array: ArrayFloat = empty_like(prototype=prices_array)
    pct_returns_array[0] = nan
    pct_returns_array[1:] = prices_array[1:] / prices_array[:-1] - 1
    return pct_returns_array


def get_total_returns(returns_array: ArrayFloat) -> ArrayFloat:
    equity_curves: ArrayFloat = get_equity_curves(
        returns_array=returns_array
    )
    return equity_curves[-1] - Standardization.PERCENTAGE.value


def get_rolling_drawdown(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    equity_curves: ArrayFloat = get_equity_curves(
        returns_array=returns_array
    )
    period_max: ArrayFloat = get_rolling_max(
        array=equity_curves, length=length, min_length=1
    )
    return (equity_curves - period_max) / period_max * Standardization.PERCENTAGE.value


def get_max_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    drawdown: ArrayFloat = get_rolling_drawdown(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return get_overall_min(array=drawdown)


def get_overall_average_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    rolling_dd: ArrayFloat = get_rolling_drawdown(
        returns_array=returns_array,
        length=returns_array.shape[0],
    )

    return get_overall_mean(array=rolling_dd)


def expanding_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:
    length: int = returns_array.shape[0]
    expanding_mean: ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=TimePeriod.HALF_YEAR.value
    )
    expanding_std: ArrayFloat = get_rolling_volatility(
        array=returns_array, length=length, min_length=TimePeriod.HALF_YEAR.value
    )
    return expanding_mean / expanding_std * Standardization.ANNUALIZATION.value


def get_rolling_sharpe_ratio(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    mean: ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=length
    )
    volatility: ArrayFloat = get_rolling_volatility(
        array=returns_array, length=length, min_length=length
    )
    return mean / volatility * Standardization.ANNUALIZATION.value


def get_overall_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:
    mean: ArrayFloat = get_overall_mean(array=returns_array)
    volatility: ArrayFloat = overall_volatility(returns_array=returns_array)
    return mean / volatility * Standardization.ANNUALIZATION.value


def get_overall_monthly_skewness(returns_array: ArrayFloat) -> ArrayFloat:
    prices_array: ArrayFloat = get_equity_curves(
        returns_array=returns_array
    )
    monthly_prices: ArrayFloat = reduce_array(
        prices_array=prices_array, frequency=TimePeriod.MONTH.value
    )
    monthly_returns: ArrayFloat = pct_returns_np(prices_array=monthly_prices)
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: ArrayFloat = get_rolling_skewness(
        array=monthly_returns, length=length_to_use, min_length=4
    )
    return get_overall_mean(array=expanding_skew)

def get_returns_distribution(returns_array: ArrayFloat, frequency: int) -> ArrayFloat:
    resampled_returns: ArrayFloat = reduce_array(
        prices_array=returns_array, frequency=frequency
    )
    return resampled_returns * Standardization.PERCENTAGE.value