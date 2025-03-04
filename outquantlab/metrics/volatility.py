import bottleneck as bn  # type: ignore
from numpy import isnan, nan, where
from outquantlab.metrics.maths_constants import ANNUALIZED_PERCENTAGE_FACTOR
from outquantlab.typing_conventions import ArrayFloat
from outquantlab.metrics.aggregation import get_overall_mean


def overall_volatility(returns_array: ArrayFloat) -> ArrayFloat:
    return bn.nanstd(returns_array, axis=0, ddof=1)  # type: ignore


def overall_volatility_annualized(returns_array: ArrayFloat) -> ArrayFloat:
    return (
        overall_volatility(returns_array=returns_array) * ANNUALIZED_PERCENTAGE_FACTOR
    )


def rolling_volatility(
    array: ArrayFloat, length: int, min_length: int = 1
) -> ArrayFloat:
    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof=1)  # type: ignore


def hv_composite(
    returns_array: ArrayFloat,
    short_term_lengths: int = 32,
    long_term_lengths: int = 1024,
    st_weight: float = 0.6,
) -> ArrayFloat:
    st_vol: ArrayFloat = rolling_volatility(
        array=returns_array, length=short_term_lengths, min_length=short_term_lengths
    )
    lt_vol: ArrayFloat = get_lt_vol(
        returns_array=returns_array, long_term_lengths=long_term_lengths
    )
    composite_vol: ArrayFloat = get_composite_vol_raw(
        st_weight=st_weight,
        short_term_vol=st_vol,
        long_term_vol=lt_vol,
    )
    return (
        get_composite_vol_filled(composite_vol=composite_vol)
        * ANNUALIZED_PERCENTAGE_FACTOR
    )


def get_lt_vol(returns_array: ArrayFloat, long_term_lengths: int) -> ArrayFloat:
    max_length: int = returns_array.shape[0]
    adjusted_length: int = (
        long_term_lengths if long_term_lengths < max_length else max_length
    )

    return rolling_volatility(array=returns_array, length=adjusted_length, min_length=1)


def get_composite_vol_raw(
    st_weight: float, short_term_vol: ArrayFloat, long_term_vol: ArrayFloat
) -> ArrayFloat:
    weighted_long_term_vol: ArrayFloat = long_term_vol * (1 - st_weight)
    weighted_short_term_vol: ArrayFloat = short_term_vol * st_weight
    return weighted_long_term_vol + weighted_short_term_vol


def get_composite_vol_filled(composite_vol: ArrayFloat) -> ArrayFloat:
    mean_vol: ArrayFloat = get_overall_mean(array=composite_vol, axis=0)
    return where(isnan(composite_vol), mean_vol, composite_vol)


def separate_volatility(
    array: ArrayFloat, len_vol: int
) -> tuple[ArrayFloat, ArrayFloat]:
    positive_returns = where(isnan(array), nan, where(array > 0, array, 0))
    negative_returns = where(isnan(array), nan, where(array < 0, array, 0))

    vol_positive: ArrayFloat = rolling_volatility(
        positive_returns, length=len_vol, min_length=1
    )
    vol_negative: ArrayFloat = rolling_volatility(
        negative_returns, length=len_vol, min_length=1
    )

    return vol_positive, vol_negative
