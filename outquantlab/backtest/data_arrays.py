from typing import NamedTuple

from numpy import empty_like, nan

from outquantlab.metrics import get_equity_curves, hv_composite, log_returns_np
from outquantlab.typing_conventions import ArrayFloat


class DataArrays(NamedTuple):
    prices: ArrayFloat
    log_returns: ArrayFloat
    adjusted_returns: ArrayFloat
    hv: ArrayFloat


def create_data_arrays(returns_array: ArrayFloat) -> DataArrays:
    prices: ArrayFloat = get_equity_curves(
        returns_array=returns_array, length=returns_array.shape[0]
    )
    returns: ArrayFloat = log_returns_np(prices_array=prices)
    hv: ArrayFloat = hv_composite(returns_array=returns_array)
    adjusted_returns: ArrayFloat = get_volatility_adjusted_returns(
        pct_returns_array=returns_array, hv_array=hv
    )
    return DataArrays(
        prices=_shift_array(original_array=prices),
        log_returns=_shift_array(original_array=returns),
        adjusted_returns=adjusted_returns,
        hv=hv,
    )


def get_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, hv_array: ArrayFloat, target_volatility: int = 25
) -> ArrayFloat:
    vol_adj_position_size_shifted: ArrayFloat = _shift_array(
        original_array=target_volatility / hv_array
    )
    return pct_returns_array * vol_adj_position_size_shifted


def _shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_like(prototype=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = nan
    return shifted_array
