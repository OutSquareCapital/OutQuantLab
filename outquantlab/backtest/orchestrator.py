from outquantlab.backtest.aggregate_returns import aggregate_raw_returns
from outquantlab.backtest.process_strategies import process_strategies
from outquantlab.indicators import BaseIndicator, ReturnsData
from outquantlab.typing_conventions import DataFrameFloat, ProgressFunc
from pandas import MultiIndex

def execute_backtest(
    indics_params: list[BaseIndicator],
    multi_index: MultiIndex,
    clusters_structure: list[str],
    returns_data: ReturnsData,
    progress_callback: ProgressFunc,
) -> None:

    raw_adjusted_returns_df: DataFrameFloat = process_strategies(
        returns_data=returns_data,
        indicators_params=indics_params,
        multi_index=multi_index,
        progress_callback=progress_callback,
    )
    (
        returns_data.global_returns,
        returns_data.sub_portfolio_roll,
        returns_data.sub_portfolio_ovrll,
    ) = aggregate_raw_returns(
        raw_adjusted_returns_df=raw_adjusted_returns_df,
        clusters_structure=clusters_structure,
        all_history=True,
        progress_callback=progress_callback,
    )