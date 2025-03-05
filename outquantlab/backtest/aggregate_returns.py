from outquantlab.backtest.data_arrays import calculate_volatility_adjusted_returns
from outquantlab.metrics import get_overall_mean, hv_composite
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat
from typing import TypedDict


class BacktestResults(TypedDict, total=False):
    portfolio: DataFrameFloat
    assets_clusters: DataFrameFloat
    assets_subclusters: DataFrameFloat
    assets: DataFrameFloat
    indics_clusters: DataFrameFloat
    indics_subclusters: DataFrameFloat
    indics: DataFrameFloat
    params: DataFrameFloat


def aggregate_raw_returns(returns_df: DataFrameFloat) -> BacktestResults:
    portfolio_dict = BacktestResults()
    clusters_depth: int = len(returns_df.columns.names)
    for lvl in range(clusters_depth, 0, -1):
        returns_df = _calculate_portfolio_returns(
            returns_df=returns_df,
            grouping_levels=returns_df.columns.names[:lvl],
        )

        returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore
        key_name: str = returns_df.columns.names[lvl - 1]
        portfolio_dict[key_name] = returns_df
    portfolio_dict["portfolio"] = _get_global_portfolio_returns(
        returns_df=_adjust_portfolio(returns_df=returns_df)
    )
    return portfolio_dict


def _adjust_portfolio(returns_df: DataFrameFloat) -> DataFrameFloat:
    array: ArrayFloat = returns_df.get_array()
    adjusted_returns: ArrayFloat = calculate_volatility_adjusted_returns(
        pct_returns_array=array,
        hv_array=hv_composite(returns_array=array, st_weight=0.1),
    )
    return DataFrameFloat(
        data=adjusted_returns, index=returns_df.dates, columns=returns_df.columns
    )


def _calculate_portfolio_returns(
    returns_df: DataFrameFloat, grouping_levels: list[str]
) -> DataFrameFloat:
    return DataFrameFloat(
        data=returns_df.T.groupby(  # type: ignore
            level=grouping_levels, observed=True
        )
        .mean()
        .T
    )


def _get_global_portfolio_returns(returns_df: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(
        data=get_overall_mean(array=returns_df.get_array(), axis=1),
        index=returns_df.dates,
        columns=["portfolio"],
    )
