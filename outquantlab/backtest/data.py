from dataclasses import dataclass, field

from outquantlab.metrics import hv_composite
from outquantlab.structures import arrays


@dataclass(slots=True)
class DataArrays:
    pct_returns: arrays.Float2D
    prices: arrays.Float2D = field(init=False)
    log_returns: arrays.Float2D = field(init=False)
    adjusted_returns: arrays.Float2D = field(init=False)

    def __post_init__(self) -> None:
        prices: arrays.Float2D = arrays.get_prices(returns=self.pct_returns)
        log_returns: arrays.Float2D = arrays.get_log_returns(prices=prices)
        hv: arrays.Float2D = hv_composite(returns_array=self.pct_returns)
        self.prices = arrays.shift(original=prices)
        self.log_returns = arrays.shift(original=log_returns)
        self.adjusted_returns = get_volatility_adjusted_returns(
            pct_returns_array=self.pct_returns, hv_array=hv
        )


def get_volatility_adjusted_returns(
    pct_returns_array: arrays.Float2D,
    hv_array: arrays.Float2D,
    target_volatility: int = 25,
) -> arrays.Float2D:
    vol_adj_position_size_shifted: arrays.Float2D = arrays.shift(
        original=target_volatility / hv_array
    )
    return pct_returns_array * vol_adj_position_size_shifted
