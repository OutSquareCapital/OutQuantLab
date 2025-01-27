from outquantlab.backtest.aggregate_returns import (
    calculate_portfolio_returns,
    get_global_portfolio_returns,
)
from outquantlab.backtest.process_strategies import (
    process_strategies,
)
from outquantlab.config_classes import (
    BacktestConfig,
    ConfigState,
)
from outquantlab.graphs import GraphsCollection
from outquantlab.indicators import DataDfs
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def execute_backtest(
    returns_df: DataFrameFloat, config: ConfigState
) -> GraphsCollection:
    data_dfs: DataDfs = DataDfs(returns_df=returns_df)

    backtest_config: BacktestConfig = config.generate_multi_index_process()

    get_strategies_returns(
        data_dfs=data_dfs,
        backtest_config=backtest_config,
    )
    aggregate_raw_returns(
        data_dfs=data_dfs,
        backtest_config=backtest_config,
    )
    print(data_dfs.global_returns)
    return GraphsCollection(data_dfs=data_dfs)


def get_strategies_returns(
    data_dfs: DataDfs,
    backtest_config: BacktestConfig,
) -> None:
    signals_array: ArrayFloat = process_strategies(
        data_arrays=data_dfs.select_data(),
        backtest_config=backtest_config,
    )
    data_dfs.global_returns = DataFrameFloat(
        data=signals_array,
        index=data_dfs.global_returns.dates,
        columns=backtest_config.multi_index,
    )


def aggregate_raw_returns(
    data_dfs: DataDfs,
    backtest_config: BacktestConfig,
) -> None:
    for lvl in range(backtest_config.clusters_nb, 0, -1):
        data_dfs.global_returns = calculate_portfolio_returns(
            returns_df=data_dfs.global_returns,
            grouping_levels=backtest_config.clusters_names[:lvl],
        )
        if lvl == 5:
            data_dfs.global_returns.dropna(axis=0, how="any", inplace=True)  # type: ignore
            data_dfs.sub_portfolio_ovrll = DataFrameFloat(data=data_dfs.global_returns)

        if lvl == 2:
            data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore
            data_dfs.sub_portfolio_roll = DataFrameFloat(data=data_dfs.global_returns)

        backtest_config.progress.get_aggregation_progress(lvl=lvl)

    data_dfs.global_returns.dropna(axis=0, how="all", inplace=True)  # type: ignore

    data_dfs.global_returns = get_global_portfolio_returns(
        returns_df=data_dfs.global_returns
    )
