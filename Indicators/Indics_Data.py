from metrics import (
    hv_composite,
    calculate_volatility_adjusted_returns,
    calculate_equity_curves,
    log_returns_np,
    shift_array,
)
from dataclasses import dataclass
from typing_conventions import ArrayFloat


@dataclass(frozen=True, slots=True)
class ReturnsData:
    log_returns_array: ArrayFloat
    prices_array: ArrayFloat
    adjusted_returns_array: ArrayFloat
    hv_array: ArrayFloat


def process_data(pct_returns_array: ArrayFloat) -> ReturnsData:
    prices_array: ArrayFloat = calculate_equity_curves(returns_array=pct_returns_array)

    hv_array: ArrayFloat = hv_composite(returns_array=pct_returns_array)

    returns_data = ReturnsData(
        log_returns_array=shift_array(
            original_array=log_returns_np(prices_array=prices_array)
        ),
        prices_array=shift_array(original_array=prices_array),
        hv_array=hv_array,
        adjusted_returns_array=calculate_volatility_adjusted_returns(
            pct_returns_array=pct_returns_array, hv_array=hv_array
        ),
    )
    return returns_data
