from outquantlab.metrics import (
    hv_composite,
    calculate_volatility_adjusted_returns,
    calculate_equity_curves,
    log_returns_np,
    shift_array,
)
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


class DataDfs:
    def __init__(self, returns_df: DataFrameFloat) -> None:
        self.global_returns: DataFrameFloat = returns_df
        self.sub_portfolio_roll: DataFrameFloat = returns_df
        self.sub_portfolio_ovrll: DataFrameFloat = returns_df

    def select_data(self, assets_names: list[str]) -> ArrayFloat:
        selected_returns = DataFrameFloat(data=self.global_returns.loc[:, assets_names])
        return selected_returns.get_array()


class DataArrays:
    def __init__(self, returns_array: ArrayFloat) -> None:
        self.log_returns_array: ArrayFloat = returns_array
        self.prices_array: ArrayFloat = returns_array
        self.adjusted_returns_array: ArrayFloat = returns_array
        self.hv_array: ArrayFloat = returns_array
        self.observations_nb: int = self.prices_array.shape[0]
        self.assets_count: int = self.prices_array.shape[1]

    def process_data(self, pct_returns_array: ArrayFloat) -> None:
        prices_array: ArrayFloat = calculate_equity_curves(
            returns_array=pct_returns_array
        )

        self.hv_array: ArrayFloat = hv_composite(returns_array=pct_returns_array)

        self.log_returns_array: ArrayFloat = shift_array(
            original_array=log_returns_np(prices_array=prices_array)
        )
        self.prices_array = shift_array(original_array=prices_array)
        self.adjusted_returns_array: ArrayFloat = calculate_volatility_adjusted_returns(
            pct_returns_array=pct_returns_array, hv_array=self.hv_array
        )
