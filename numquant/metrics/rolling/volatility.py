from numquant.main import Float2D
from numquant.metrics.constants import Period, ANNUALIZED_PERCENTAGE
import bottleneck as bn  # type: ignore
from numquant.arrays import fill_nan_with_data
from numquant.metrics.aggregate import get_mean

def get_volatility(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof=1)  # type: ignore

def get_volatility_annualized(
    array: Float2D, length: int, min_length: int = 1
) -> Float2D:
    return (
        get_volatility(array=array, length=length, min_length=min_length)
        * ANNUALIZED_PERCENTAGE
    )

def hv_composite(
    returns_array: Float2D,
    short_term_lengths: int = Period.MONTH,
    long_term_lengths: int = Period.HALF_DECADE,
    st_weight: float = 0.6,
) -> Float2D:
    st_vol: Float2D = get_volatility(
        array=returns_array, length=short_term_lengths, min_length=short_term_lengths
    )
    lt_vol: Float2D = get_lt_vol(
        returns_array=returns_array, long_term_lengths=long_term_lengths
    )
    composite_vol: Float2D = get_composite_vol_raw(
        st_weight=st_weight,
        short_term_vol=st_vol,
        long_term_vol=lt_vol,
    )
    return (
        get_composite_vol_filled(composite_vol=composite_vol) * ANNUALIZED_PERCENTAGE
    )


def get_lt_vol(returns_array: Float2D, long_term_lengths: int) -> Float2D:
    max_length: int = returns_array.shape[0]
    adjusted_length: int = (
        long_term_lengths if long_term_lengths < max_length else max_length
    )

    return get_volatility(
        array=returns_array, length=adjusted_length, min_length=1
    )


def get_composite_vol_raw(
    st_weight: float, short_term_vol: Float2D, long_term_vol: Float2D
) -> Float2D:
    weighted_long_term_vol: Float2D = long_term_vol * (1 - st_weight)
    weighted_short_term_vol: Float2D = short_term_vol * st_weight
    return weighted_long_term_vol + weighted_short_term_vol


def get_composite_vol_filled(composite_vol: Float2D) -> Float2D:
    mean_vol: Float2D = get_mean(array=composite_vol, axis=0)
    return fill_nan_with_data(base_array=composite_vol, array_filler=mean_vol)