import bottleneck as bn  # type: ignore
from numpy import isnan, where

from outquantlab.metrics.aggregation import get_overall_mean
from outquantlab.metrics.maths_constants import ANNUALIZED_PERCENTAGE, TimePeriod
from outquantlab.structures import arrays


def overall_volatility(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    return bn.nanstd(returns_array, axis=0, ddof=1)  # type: ignore


def get_overall_volatility_annualized(returns_array: arrays.ArrayFloat) -> arrays.ArrayFloat:
    return overall_volatility(returns_array=returns_array) * ANNUALIZED_PERCENTAGE


def get_rolling_volatility(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof=1)  # type: ignore


def get_rolling_volatility_annualized(
    array: arrays.ArrayFloat, length: int, min_length: int = 1
) -> arrays.ArrayFloat:
    return (
        get_rolling_volatility(array=array, length=length, min_length=min_length)
        * ANNUALIZED_PERCENTAGE
    )


def hv_composite(
    returns_array: arrays.ArrayFloat,
    short_term_lengths: int = TimePeriod.MONTH,
    long_term_lengths: int = TimePeriod.HALF_DECADE,
    st_weight: float = 0.6,
) -> arrays.ArrayFloat:
    st_vol: arrays.ArrayFloat = get_rolling_volatility(
        array=returns_array, length=short_term_lengths, min_length=short_term_lengths
    )
    lt_vol: arrays.ArrayFloat = get_lt_vol(
        returns_array=returns_array, long_term_lengths=long_term_lengths
    )
    composite_vol: arrays.ArrayFloat = get_composite_vol_raw(
        st_weight=st_weight,
        short_term_vol=st_vol,
        long_term_vol=lt_vol,
    )
    return get_composite_vol_filled(composite_vol=composite_vol) * ANNUALIZED_PERCENTAGE


def get_lt_vol(returns_array: arrays.ArrayFloat, long_term_lengths: int) -> arrays.ArrayFloat:
    max_length: int = returns_array.shape[0]
    adjusted_length: int = (
        long_term_lengths if long_term_lengths < max_length else max_length
    )

    return get_rolling_volatility(
        array=returns_array, length=adjusted_length, min_length=1
    )


def get_composite_vol_raw(
    st_weight: float, short_term_vol: arrays.ArrayFloat, long_term_vol: arrays.ArrayFloat
) -> arrays.ArrayFloat:
    weighted_long_term_vol: arrays.ArrayFloat = long_term_vol * (1 - st_weight)
    weighted_short_term_vol: arrays.ArrayFloat = short_term_vol * st_weight
    return weighted_long_term_vol + weighted_short_term_vol


def get_composite_vol_filled(composite_vol: arrays.ArrayFloat) -> arrays.ArrayFloat:
    mean_vol: arrays.ArrayFloat = get_overall_mean(array=composite_vol, axis=0)
    return where(isnan(composite_vol), mean_vol, composite_vol)


def separate_volatility(
    array: arrays.ArrayFloat, len_vol: int
) -> tuple[arrays.ArrayFloat, arrays.ArrayFloat]:
    positive_returns = where(isnan(array), arrays.Nan, where(array > 0, array, 0))
    negative_returns = where(isnan(array), arrays.Nan, where(array < 0, array, 0))

    vol_positive: arrays.ArrayFloat = get_rolling_volatility(
        positive_returns, length=len_vol, min_length=1
    )
    vol_negative: arrays.ArrayFloat = get_rolling_volatility(
        negative_returns, length=len_vol, min_length=1
    )

    return vol_positive, vol_negative
