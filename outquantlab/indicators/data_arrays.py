from numpy import empty_like, nan

from outquantlab.metrics import get_equity_curves, hv_composite, log_returns_np
from outquantlab.structures import ArrayFloat
from dataclasses import dataclass, field


@dataclass(slots=True)
class DataArrays:
    pct_returns: ArrayFloat
    prices: ArrayFloat = field(init=False)
    log_returns: ArrayFloat = field(init=False)
    adjusted_returns: ArrayFloat = field(init=False)
    hv: ArrayFloat = field(init=False)

    def __post_init__(self) -> None:
        prices: ArrayFloat = get_equity_curves(returns_array=self.pct_returns)
        returns: ArrayFloat = log_returns_np(prices_array=prices)
        self.hv: ArrayFloat = hv_composite(returns_array=self.pct_returns)
        self.adjusted_returns: ArrayFloat = get_volatility_adjusted_returns(
            pct_returns_array=self.pct_returns, hv_array=self.hv
        )
        self.pct_returns = _shift_array(original_array=self.pct_returns)
        self.prices = _shift_array(original_array=prices)
        self.log_returns = _shift_array(original_array=returns)


def get_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, hv_array: ArrayFloat, target_volatility: int = 25
) -> ArrayFloat:
    vol_adj_position_size_shifted: ArrayFloat = _shift_array(
        original_array=target_volatility / (hv_array + 1e-10)
    )
    return pct_returns_array * vol_adj_position_size_shifted


def _shift_array(original_array: ArrayFloat, step: int = 1) -> ArrayFloat:
    shifted_array: ArrayFloat = empty_like(prototype=original_array)
    shifted_array[step:, :] = original_array[:-step, :]
    shifted_array[:step, :] = nan
    return shifted_array
