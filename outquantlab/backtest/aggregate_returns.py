from outquantlab.metrics import calculate_overall_mean
from outquantlab.typing_conventions import DataFrameFloat


def calculate_portfolio_returns(
    returns_df: DataFrameFloat, grouping_levels: list[str]
) -> DataFrameFloat:
    return DataFrameFloat(
        data=returns_df.T.groupby(  # type: ignore
            level=grouping_levels, observed=True
        )
        .mean()
        .T
    )


def get_global_portfolio_returns(returns_df: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(
        data=calculate_overall_mean(array=returns_df.get_array(), axis=1),
        index=returns_df.dates,
        columns=["Portfolio"],
    )