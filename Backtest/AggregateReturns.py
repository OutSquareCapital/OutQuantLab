
from TypingConventions import ProgressFunc, DataFrameFloat
from Metrics import calculate_overall_mean

def calculate_portfolio_returns(
    returns_df: DataFrameFloat,
    grouping_levels: list[str]
    ) -> DataFrameFloat:

    return DataFrameFloat(
        data=returns_df
        .T
        .groupby(level=grouping_levels, observed=True) # type: ignore
        .mean()
        .T
        )

def aggregate_raw_returns(
    raw_adjusted_returns_df: DataFrameFloat,
    clusters_structure: list[str],
    all_history: bool,
    progress_callback: ProgressFunc
) -> tuple[DataFrameFloat, DataFrameFloat, DataFrameFloat]:

    if not all_history:
        raw_adjusted_returns_df.dropna(axis=0, how='any', inplace=True)  # type: ignore
    clusters_nb: int = len(clusters_structure) - 1
    for i in range(clusters_nb, 0, -1):
        grouping_levels: list[str] = clusters_structure[:i]

        raw_adjusted_returns_df = calculate_portfolio_returns(
            returns_df=raw_adjusted_returns_df,
            grouping_levels=grouping_levels
        )
        if i == 5:
            raw_adjusted_returns_df.dropna(axis=0, how='any', inplace=True)  # type: ignore
            sub_portfolio_overall = DataFrameFloat(data=raw_adjusted_returns_df)

        if i == 2:
            raw_adjusted_returns_df.dropna(axis=0, how='all', inplace=True)  # type: ignore
            sub_portfolio_rolling = DataFrameFloat(data=raw_adjusted_returns_df)

        progress_callback(
            int(100 * (clusters_nb - i) / clusters_nb),
            f"Aggregating {' > '.join(grouping_levels)}: {len(raw_adjusted_returns_df.columns)} columns left..."
        )
    progress_callback(100, "Backtest Completed!")

    raw_adjusted_returns_df.dropna(axis=0, how='all', inplace=True)  # type: ignore

    return DataFrameFloat(
        data=calculate_overall_mean(array=raw_adjusted_returns_df.nparray, axis=1),
        index=raw_adjusted_returns_df.dates,
        columns=['Portfolio']
        ), sub_portfolio_rolling, sub_portfolio_overall # type: ignore