
from outquantlab.metrics import hv_composite
from outquantlab.structures import ArrayFloat, log_returns_array, shift_array, get_prices_array
from typing import NamedTuple


class DataArrays(NamedTuple):
    pct_returns: ArrayFloat
    prices: ArrayFloat
    log_returns: ArrayFloat
    adjusted_returns: ArrayFloat


def get_data_arrays(pct_returns: ArrayFloat) -> DataArrays:
    prices: ArrayFloat = get_prices_array(returns_array=pct_returns)
    log_returns: ArrayFloat = log_returns_array(prices_array=prices)
    hv: ArrayFloat = hv_composite(returns_array=pct_returns)
    return DataArrays(
        pct_returns=pct_returns,
        prices=shift_array(original_array=prices),
        log_returns=shift_array(original_array=log_returns),
        adjusted_returns=get_volatility_adjusted_returns(
            pct_returns_array=pct_returns, hv_array=hv
        )
    )


def get_volatility_adjusted_returns(
    pct_returns_array: ArrayFloat, hv_array: ArrayFloat, target_volatility: int = 25
) -> ArrayFloat:
    vol_adj_position_size_shifted: ArrayFloat = shift_array(
        original_array=target_volatility / (hv_array + 1e-10)
    )
    return pct_returns_array * vol_adj_position_size_shifted



