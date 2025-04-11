import bottleneck as bn  # type: ignore

from numquant.main import Float2D
from numquant.constants import ANNUALIZED_PERCENTAGE


def get_mean(array: Float2D, axis: None | int = 0) -> Float2D:
    return bn.nanmean(array, axis)  # type: ignore


def get_median(array: Float2D, axis: None | int = 0) -> Float2D:
    return bn.nanmedian(array, axis)  # type: ignore


def get_volatility(returns_array: Float2D) -> Float2D:
    return bn.nanstd(returns_array, axis=0, ddof=1)  # type: ignore

def get_volatility_annualized(returns_array: Float2D) -> Float2D:
    return get_volatility(returns_array=returns_array) * ANNUALIZED_PERCENTAGE


def get_max(array: Float2D, axis: int = 0) -> Float2D:
    return bn.nanmax(array, axis)  # type: ignore


def get_min(array: Float2D, axis: int = 0) -> Float2D:
    return bn.nanmin(array, axis)  # type: ignore