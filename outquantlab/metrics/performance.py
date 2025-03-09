from outquantlab.typing_conventions import ArrayFloat, ArrayInt
from outquantlab.metrics.maths_constants import ANNUALIZATION_FACTOR, PERCENTAGE_FACTOR
from outquantlab.metrics.aggregation import (
    get_rolling_mean,
    get_overall_mean,
    get_rolling_max,
    get_overall_min,
)
from outquantlab.metrics.volatility import rolling_volatility, overall_volatility
from outquantlab.metrics.distribution import rolling_skewness
from numpy import log, nan, cumprod, arange, append, empty_like, isnan


def reduce_array(prices_array: ArrayFloat, frequency: int) -> ArrayFloat:
    array_length: int = prices_array.shape[0]
    indices: ArrayInt = arange(start=0, stop=array_length, step=frequency)

    if array_length % frequency != 0:
        indices: ArrayInt = append(arr=indices, values=array_length - 1)
    return prices_array[indices]


def calculate_equity_curves(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    start: int = returns_array.shape[0] - length
    temp_array: ArrayFloat = returns_array.copy()
    mask: ArrayFloat = isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns: ArrayFloat = empty_like(prototype=temp_array)

    cumulative_returns[:start] = nan

    cumulative_returns[start:] = cumprod(a=1 + temp_array[start:], axis=0)

    cumulative_returns[mask] = nan

    return cumulative_returns * PERCENTAGE_FACTOR


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


def calculate_total_returns(returns_array: ArrayFloat) -> ArrayFloat:
    equity_curves: ArrayFloat = calculate_equity_curves(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return equity_curves[-1] - 100


def calculate_rolling_drawdown(returns_array: ArrayFloat, length: int) -> ArrayFloat:
    equity_curves: ArrayFloat = calculate_equity_curves(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    period_max: ArrayFloat = get_rolling_max(
        array=equity_curves, length=length, min_length=1
    )
    return (equity_curves - period_max) / period_max * PERCENTAGE_FACTOR


def calculate_max_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    drawdown: ArrayFloat = calculate_rolling_drawdown(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    return get_overall_min(array=drawdown)


def calculate_overall_average_drawdown(returns_array: ArrayFloat) -> ArrayFloat:
    rolling_dd: ArrayFloat = calculate_rolling_drawdown(
        returns_array=returns_array,
        length=returns_array.shape[0],
    )

    return get_overall_mean(array=rolling_dd)


def expanding_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:
    length: int = returns_array.shape[0]
    expanding_mean: ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=125
    )
    expanding_std: ArrayFloat = rolling_volatility(
        array=returns_array, length=length, min_length=125
    )
    return expanding_mean / expanding_std * ANNUALIZATION_FACTOR


def rolling_sharpe_ratio(
    returns_array: ArrayFloat, length: int, min_length: int = 20
) -> ArrayFloat:
    mean: ArrayFloat = get_rolling_mean(
        array=returns_array, length=length, min_length=min_length
    )
    volatility: ArrayFloat = rolling_volatility(
        array=returns_array, length=length, min_length=min_length
    )
    return mean / volatility * ANNUALIZATION_FACTOR


def overall_sharpe_ratio(returns_array: ArrayFloat) -> ArrayFloat:
    mean: ArrayFloat = get_overall_mean(array=returns_array)
    volatility: ArrayFloat = overall_volatility(returns_array=returns_array)
    return mean / volatility * ANNUALIZATION_FACTOR


def calculate_overall_monthly_skewness(returns_array: ArrayFloat) -> ArrayFloat:
    prices_array: ArrayFloat = calculate_equity_curves(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    monthly_prices: ArrayFloat = reduce_array(prices_array=prices_array, frequency=21)
    monthly_returns: ArrayFloat = pct_returns_np(prices_array=monthly_prices)
    length_to_use: int = monthly_returns.shape[0]
    expanding_skew: ArrayFloat = rolling_skewness(
        array=monthly_returns, length=length_to_use, min_length=4
    )
    return get_overall_mean(array=expanding_skew)
