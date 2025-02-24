from outquantlab.metrics import (
    calculate_equity_curves,
    hv_composite,
    log_returns_np
)
from outquantlab.typing_conventions import ArrayFloat
from numpy import empty_like, nan

class DataArrays:
    def __init__(self, returns_array: ArrayFloat) -> None:
        self.prices_array: ArrayFloat = calculate_equity_curves(
            returns_array=returns_array
        )

        self.hv_array: ArrayFloat = hv_composite(returns_array=returns_array)

        self.log_returns_array: ArrayFloat = shift_array(
            original_array=log_returns_np(prices_array=self.prices_array)
        )
        self.prices_array: ArrayFloat = shift_array(original_array=self.prices_array)
        self.adjusted_returns_array: ArrayFloat = calculate_volatility_adjusted_returns(
            pct_returns_array=returns_array, hv_array=self.hv_array
        )

def calculate_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, hv_array: ArrayFloat, target_volatility: int = 15
) -> ArrayFloat:
    vol_adj_position_size = target_volatility / hv_array
    
    vol_adj_position_size_shifted: ArrayFloat = shift_array(
        original_array=vol_adj_position_size
    )
    return pct_returns_array * vol_adj_position_size_shifted

def shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_like(prototype=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = nan
    return shifted_array