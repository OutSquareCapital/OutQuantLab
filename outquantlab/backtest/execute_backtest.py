from outquantlab.backtest.aggregate_returns import (
    calculate_portfolio_returns,
    get_global_portfolio_returns,
)
from outquantlab.backtest.process_strategies import process_strategies
from outquantlab.config_classes import BacktestConfig
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat
from outquantlab.backtest.data_arrays import DataArrays

def execute_backtest(
    returns_df: DataFrameFloat, backtest_config: BacktestConfig
) -> dict[str, DataFrameFloat]:
    returns_df = get_strategies_returns(
        returns_df=returns_df,
        backtest_config=backtest_config,
    )
    return aggregate_raw_returns(returns_df=returns_df)


def get_strategies_returns(
    returns_df: DataFrameFloat,
    backtest_config: BacktestConfig,
) -> DataFrameFloat:
    results_array: ArrayFloat = process_strategies(
        data_arrays=DataArrays(returns_array=returns_df.get_array()),
        backtest_config=backtest_config,
    )
    return DataFrameFloat(
        data=results_array,
        index=returns_df.dates,
        columns=backtest_config.multi_index,
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
