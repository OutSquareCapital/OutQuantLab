from outquantlab.config_classes import ProgressStatus
from outquantlab.indicators import DataDfs
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


def aggregate_raw_returns(
    clusters_nb: int,
    clusters_names: list[str],
    data_dfs: DataDfs,
    progress: ProgressStatus,
) -> None:
    for lvl in range(clusters_nb, 0, -1):
        data_dfs.global_returns = calculate_portfolio_returns(
            returns_df=data_dfs.global_returns, grouping_levels=clusters_names[:lvl]
        )
        if lvl == 5:
            data_dfs.global_returns.dropna(axis=0, how="any", inplace=True)  # type: ignore
            data_dfs.sub_portfolio_ovrll = DataFrameFloat(data=data_dfs.global_returns)

        if lvl == 2:
            data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore
            data_dfs.sub_portfolio_roll = DataFrameFloat(data=data_dfs.global_returns)

        progress.get_aggregation_progress(lvl=lvl)

    data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore

    data_dfs.global_returns = get_global_portfolio_returns(
        returns_df=data_dfs.global_returns
    )
