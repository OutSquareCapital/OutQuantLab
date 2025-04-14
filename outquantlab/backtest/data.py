from dataclasses import dataclass, field
import numquant as nq

@dataclass(slots=True)
class DataArrays:
    pct_returns: nq.Float2D
    prices: nq.Float2D = field(init=False)
    log_returns: nq.Float2D = field(init=False)
    adjusted_returns: nq.Float2D = field(init=False)

    def __post_init__(self) -> None:
        prices: nq.Float2D = nq.arrays.get_prices(returns=self.pct_returns)
        log_returns: nq.Float2D = nq.arrays.get_log_returns(prices=prices)
        hv: nq.Float2D = nq.metrics.roll.get_composite_volatility(returns_array=self.pct_returns)
        self.prices = nq.arrays.shift(original=prices)
        self.log_returns = nq.arrays.shift(original=log_returns)
        self.adjusted_returns = get_volatility_adjusted_returns(
            pct_returns_array=self.pct_returns, hv_array=hv
        )


def get_volatility_adjusted_returns(
    pct_returns_array: nq.Float2D,
    hv_array: nq.Float2D,
    target_volatility: int = 25,
) -> nq.Float2D:
    vol_adj_position_size_shifted: nq.Float2D = nq.arrays.shift(
        original=target_volatility / hv_array
    )
    return pct_returns_array * vol_adj_position_size_shifted
