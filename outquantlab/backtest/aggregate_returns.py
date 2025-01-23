
from outquantlab.typing_conventions import ArrayFloat, ProgressFunc, DataFrameFloat
from outquantlab.metrics import calculate_overall_mean
from outquantlab.backtest.backtest_specs import BacktestSpecs

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
    signals_array: ArrayFloat,
    backtest_specs: BacktestSpecs,
    progress_callback: ProgressFunc
) -> tuple[DataFrameFloat, DataFrameFloat, DataFrameFloat]:
    raw_adjusted_returns_df = DataFrameFloat(
            data=signals_array, index=backtest_specs.dates, columns=backtest_specs.multi_index
        )
    del signals_array
    clusters_nb: int = len(backtest_specs.multi_index.names) - 1
    for i in range(clusters_nb, 0, -1):
        grouping_levels: list[str] = backtest_specs.multi_index.names[:i]
        raw_adjusted_returns_df: DataFrameFloat = calculate_portfolio_returns(
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
        data=calculate_overall_mean(array=raw_adjusted_returns_df.get_array(), axis=1),
        index=raw_adjusted_returns_df.dates,
        columns=['Portfolio']
        ), sub_portfolio_rolling, sub_portfolio_overall # type: ignore