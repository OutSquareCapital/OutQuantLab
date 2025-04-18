import bottleneck as bn  # type: ignore

from numquant.arrays import fill_nan_with_data
from numquant.main import Float2D
from numquant.metrics.aggregate import get_mean
from numquant.metrics.constants import ANNUALIZED_PERCENTAGE, ANNUALIZATION,  Period


def get_volatility(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof=1)  # type: ignore


def get_expanding_volatility(array: Float2D, min_length: int = 1) -> Float2D:
    return get_volatility(array=array, length=array.shape[0], min_length=min_length)

def get_expanding_volatility_annualized(
    array: Float2D, min_length: int = 1
) -> Float2D:
    return get_expanding_volatility(array=array, min_length=min_length) * ANNUALIZATION

def get_expanding_volatility_annualized_pct(
    array: Float2D, min_length: int = 1
) -> Float2D:
    return get_expanding_volatility(array=array, min_length=min_length) * ANNUALIZED_PERCENTAGE

def get_volatility_annualized(
    array: Float2D, length: int, min_length: int = 1
) -> Float2D:
    return (
        get_volatility(array=array, length=length, min_length=min_length)
        * ANNUALIZATION
    )

def get_volatility_annualized_pct(
    array: Float2D, length: int, min_length: int = 1
) -> Float2D:
    return (
        get_volatility(array=array, length=length, min_length=min_length)
        * ANNUALIZED_PERCENTAGE
    )

def get_composite_volatility(
    returns_array: Float2D,
    short_term_lengths: int = Period.MONTH,
    st_weight: float = 0.6,
) -> Float2D:
    st_vol: Float2D = get_volatility_annualized_pct(
        array=returns_array, length=short_term_lengths, min_length=short_term_lengths
    )
    lt_vol: Float2D = get_expanding_volatility_annualized_pct(
        array=returns_array, min_length=short_term_lengths
    )
    composite_vol: Float2D = get_composite_vol_raw(
        st_weight=st_weight,
        short_term_vol=st_vol,
        long_term_vol=lt_vol,
    )
    return get_composite_vol_filled(composite_vol=composite_vol)


def get_composite_vol_raw(
    st_weight: float, short_term_vol: Float2D, long_term_vol: Float2D
) -> Float2D:
    weighted_long_term_vol: Float2D = long_term_vol * (1 - st_weight)
    weighted_short_term_vol: Float2D = short_term_vol * st_weight
    return weighted_long_term_vol + weighted_short_term_vol


def get_composite_vol_filled(composite_vol: Float2D) -> Float2D:
    mean_vol: Float2D = get_mean(array=composite_vol, axis=0)
    return fill_nan_with_data(base_array=composite_vol, array_filler=mean_vol)
