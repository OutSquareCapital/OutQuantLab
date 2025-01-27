from dataclasses import dataclass

from outquantlab.metrics import (
    calculate_equity_curves,
    calculate_volatility_adjusted_returns,
    hv_composite,
    log_returns_np,
    shift_array,
)
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


@dataclass(slots=True, frozen=True)
class DataArrays:
    prices_array: ArrayFloat
    log_returns_array: ArrayFloat
    adjusted_returns_array: ArrayFloat
    hv_array: ArrayFloat


class DataDfs:
    def __init__(self, returns_df: DataFrameFloat) -> None:
        self.global_returns: DataFrameFloat = returns_df
        self.sub_portfolio_roll: DataFrameFloat = returns_df
        self.sub_portfolio_ovrll: DataFrameFloat = returns_df

    def select_data(self) -> DataArrays:
        returns_array: ArrayFloat = self.global_returns.get_array()
        prices_array: ArrayFloat = calculate_equity_curves(returns_array=returns_array)

        hv_array: ArrayFloat = hv_composite(returns_array=returns_array)

        log_returns_array: ArrayFloat = shift_array(
            original_array=log_returns_np(prices_array=prices_array)
        )
        prices_array: ArrayFloat = shift_array(original_array=prices_array)
        adjusted_returns_array: ArrayFloat = calculate_volatility_adjusted_returns(
            pct_returns_array=returns_array, hv_array=hv_array
        )

        return DataArrays(
            prices_array=prices_array,
            log_returns_array=log_returns_array,
            adjusted_returns_array=adjusted_returns_array,
            hv_array=hv_array,
        )
