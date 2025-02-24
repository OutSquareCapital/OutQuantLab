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

def aggregate_raw_returns(returns_df: DataFrameFloat) -> dict[str, DataFrameFloat]:
    portfolio_dict: dict[str, DataFrameFloat] = {}
    clusters_depth: int = len(returns_df.columns.names)
    for lvl in range(clusters_depth, 0, -1):
        returns_df = calculate_portfolio_returns(
            returns_df=returns_df,
            grouping_levels=returns_df.columns.names[:lvl],
        )

        returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore
        key_name: str = returns_df.columns.names[lvl - 1]
        portfolio_dict[key_name] = returns_df

    portfolio_dict["lvl0"] = get_global_portfolio_returns(returns_df=returns_df)

    return portfolio_dict