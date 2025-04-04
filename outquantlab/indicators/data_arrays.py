from typing import NamedTuple

from outquantlab.metrics import hv_composite
from outquantlab.structures import arrays


class DataArrays(NamedTuple):
    pct_returns: arrays.Float2D
    prices: arrays.Float2D
    log_returns: arrays.Float2D
    adjusted_returns: arrays.Float2D


def get_data_arrays(pct_returns: arrays.Float2D) -> DataArrays:
    prices: arrays.Float2D = arrays.get_prices(returns=pct_returns)
    log_returns: arrays.Float2D = arrays.get_log_returns(prices=prices)
    hv: arrays.Float2D = hv_composite(returns_array=pct_returns)
    return DataArrays(
        pct_returns=pct_returns,
        prices=arrays.shift(original=prices),
        log_returns=arrays.shift(original=log_returns),
        adjusted_returns=get_volatility_adjusted_returns(
            pct_returns_array=pct_returns, hv_array=hv
        ),
    )


def get_volatility_adjusted_returns(
    pct_returns_array: arrays.Float2D,
    hv_array: arrays.Float2D,
    target_volatility: int = 25,
) -> arrays.Float2D:
    vol_adj_position_size_shifted: arrays.Float2D = arrays.shift(
        original=target_volatility / (hv_array + 1e-10)
    )
    return pct_returns_array * vol_adj_position_size_shifted
