from outquantlab.backtest.aggregate_returns import (
    calculate_portfolio_returns,
    get_global_portfolio_returns,
)
from outquantlab.backtest.process_strategies import process_strategies
from outquantlab.config_classes import BacktestConfig
from outquantlab.indicators import get_data_arrays
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def execute_backtest(
    returns_df: DataFrameFloat, backtest_config: BacktestConfig
) -> dict[str, DataFrameFloat]:
    returns_df = get_strategies_returns(
        returns_df=returns_df,
        backtest_config=backtest_config,
    )
    return aggregate_raw_returns(
        returns_df=returns_df,
        backtest_config=backtest_config,
    )


def get_strategies_returns(
    returns_df: DataFrameFloat,
    backtest_config: BacktestConfig,
) -> DataFrameFloat:
    signals_array: ArrayFloat = process_strategies(
        data_arrays=get_data_arrays(returns_array=returns_df.get_array()),
        backtest_config=backtest_config,
    )
    return DataFrameFloat(
        data=signals_array,
        index=returns_df.dates,
        columns=backtest_config.multi_index,
    )


def aggregate_raw_returns(
    returns_df: DataFrameFloat,
    backtest_config: BacktestConfig,
) -> dict[str, DataFrameFloat]:
    portfolio_dict: dict[str, DataFrameFloat] = {}

    for lvl in range(backtest_config.clusters_nb, 0, -1):
        returns_df = calculate_portfolio_returns(
            returns_df=returns_df,
            grouping_levels=backtest_config.clusters_names[:lvl],
        )

        returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore

        portfolio_dict[backtest_config.clusters_names[lvl - 1]] = returns_df

        returns_df.dropna(axis=0, how="all", inplace=True)  # type: ignore

        backtest_config.progress.get_aggregation_progress(
            lvl=lvl, clusters_nb=backtest_config.clusters_nb
        )

    portfolio_dict["lvl0"] = get_global_portfolio_returns(returns_df=returns_df)

    return portfolio_dict
