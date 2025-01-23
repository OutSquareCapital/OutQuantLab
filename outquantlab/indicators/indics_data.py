from outquantlab.metrics import (
    hv_composite,
    calculate_volatility_adjusted_returns,
    calculate_equity_curves,
    log_returns_np,
    shift_array,
)
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat

class ReturnsData:
    def __init__(self, returns_df: DataFrameFloat) -> None:
        returns_array = returns_df.get_array()
        self.log_returns_array: ArrayFloat = returns_array
        self.prices_array: ArrayFloat = returns_array
        self.adjusted_returns_array: ArrayFloat = returns_array
        self.hv_array: ArrayFloat = returns_array
        self.global_returns: DataFrameFloat = returns_df
        self.sub_portfolio_roll: DataFrameFloat = returns_df
        self.sub_portfolio_ovrll: DataFrameFloat = returns_df

    def process_data(self, pct_returns_array: ArrayFloat) -> None:
        prices_array: ArrayFloat = calculate_equity_curves(returns_array=pct_returns_array)

        self.hv_array: ArrayFloat = hv_composite(returns_array=pct_returns_array)

        self.log_returns_array: ArrayFloat=shift_array(
            original_array=log_returns_np(prices_array=prices_array)
        )
        self.prices_array=shift_array(original_array=prices_array)
        self.adjusted_returns_array: ArrayFloat =calculate_volatility_adjusted_returns(
            pct_returns_array=pct_returns_array, hv_array=self.hv_array
        )