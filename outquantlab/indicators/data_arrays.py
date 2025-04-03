from typing import NamedTuple

from outquantlab.metrics import hv_composite
from outquantlab.structures import arrays


class DataArrays(NamedTuple):
    pct_returns: arrays.ArrayFloat
    prices: arrays.ArrayFloat
    log_returns: arrays.ArrayFloat
    adjusted_returns: arrays.ArrayFloat


def get_data_arrays(pct_returns: arrays.ArrayFloat) -> DataArrays:
    prices: arrays.ArrayFloat = arrays.get_prices_array(returns_array=pct_returns)
    log_returns: arrays.ArrayFloat = arrays.log_returns_array(prices_array=prices)
    hv: arrays.ArrayFloat = hv_composite(returns_array=pct_returns)
    return DataArrays(
        pct_returns=pct_returns,
        prices=arrays.shift_array(original_array=prices),
        log_returns=arrays.shift_array(original_array=log_returns),
        adjusted_returns=get_volatility_adjusted_returns(
            pct_returns_array=pct_returns, hv_array=hv
        ),
    )


def get_volatility_adjusted_returns(
    pct_returns_array: arrays.ArrayFloat,
    hv_array: arrays.ArrayFloat,
    target_volatility: int = 25,
) -> arrays.ArrayFloat:
    vol_adj_position_size_shifted: arrays.ArrayFloat = arrays.shift_array(
        original_array=target_volatility / (hv_array + 1e-10)
    )
    return pct_returns_array * vol_adj_position_size_shifted
