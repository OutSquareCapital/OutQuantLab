from typing import NamedTuple

from numpy import empty_like, nan

from outquantlab.metrics import calculate_equity_curves, hv_composite, log_returns_np
from outquantlab.typing_conventions import ArrayFloat


class DataArrays(NamedTuple):
    prices: ArrayFloat
    hv: ArrayFloat
    log_returns: ArrayFloat
    adjusted_returns: ArrayFloat


def create_data_arrays(returns_array: ArrayFloat) -> DataArrays:
    prices: ArrayFloat = calculate_equity_curves(returns_array=returns_array)
    hv: ArrayFloat = hv_composite(returns_array=returns_array)
    log_returns: ArrayFloat = _shift_array(
        original_array=log_returns_np(prices_array=prices)
    )
    prices_shifted: ArrayFloat = _shift_array(original_array=prices)
    adjusted_returns: ArrayFloat = calculate_volatility_adjusted_returns(
        pct_returns_array=returns_array, hv_array=hv
    )
    return DataArrays(
        prices=prices_shifted,
        hv=hv,
        log_returns=log_returns,
        adjusted_returns=adjusted_returns,
    )


def calculate_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, hv_array: ArrayFloat, target_volatility: int = 25
) -> ArrayFloat:
    vol_adj_position_size = target_volatility / hv_array

    vol_adj_position_size_shifted: ArrayFloat = _shift_array(
        original_array=vol_adj_position_size
    )
    return pct_returns_array * vol_adj_position_size_shifted


def _shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_like(prototype=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = nan
    return shifted_array
