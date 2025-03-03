from outquantlab.backtest.aggregate_returns import aggregate_raw_returns
from outquantlab.backtest.data_arrays import create_data_arrays
from outquantlab.backtest.process_strategies import process_strategies
from outquantlab.config_classes import BacktestConfig
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def execute_backtest(
    returns_df: DataFrameFloat, backtest_config: BacktestConfig
) -> dict[str, DataFrameFloat]:
    returns_df = _get_strategies_returns(
        returns_df=returns_df,
        backtest_config=backtest_config,
    )
    return aggregate_raw_returns(returns_df=returns_df)


def _get_strategies_returns(
    returns_df: DataFrameFloat,
    backtest_config: BacktestConfig,
) -> DataFrameFloat:
    results_array: ArrayFloat = process_strategies(
        data_arrays=create_data_arrays(returns_array=returns_df.get_array()),
        backtest_config=backtest_config,
    )
    return DataFrameFloat(
        data=results_array,
        index=returns_df.dates,
        columns=backtest_config.multi_index,
    )
