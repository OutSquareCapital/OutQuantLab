
import numpy as np
import pandas as pd
from DataBase import N_THREADS
from Utilitary import ArrayFloat, ProgressFunc, DataFrameFloat, Float32
from concurrent.futures import ThreadPoolExecutor
from ConfigClasses import Indicator
from Indicators import IndicatorsMethods
from Metrics import calculate_overall_mean
from Backtest.Sharpe_Optimization import relative_sharpe_on_confidence_period

def calculate_strategy_returns(
    pct_returns_array: ArrayFloat, 
    indicators_params: list[Indicator],
    indics_methods: IndicatorsMethods,
    dates_index: pd.DatetimeIndex,
    multi_index: pd.MultiIndex,
    progress_callback: ProgressFunc
    ) -> DataFrameFloat:
    signal_col_index = 0
    global_executor = ThreadPoolExecutor(max_workers=N_THREADS)
    indics_methods.process_data(pct_returns_array=pct_returns_array)
    total_assets_count: int = pct_returns_array.shape[1]
    total_returns_streams: int = total_assets_count * sum([indic.strategies_nb for indic in indicators_params])
    signals_array: ArrayFloat = np.empty(shape=(pct_returns_array.shape[0], total_returns_streams), dtype=Float32)

    for indic in indicators_params:
        results: list[ArrayFloat] = indics_methods.process_indicator_parallel(
            func=indic.func, 
            params=indic.param_combos, 
            global_executor=global_executor
        )

        for result in results:
            signals_array[:, signal_col_index:signal_col_index + total_assets_count] = result
            signal_col_index += total_assets_count

        progress_callback(
            int(100 * signal_col_index / total_returns_streams),
            f"Backtesting Strategies: {signal_col_index}/{total_returns_streams}..."
        )

    return DataFrameFloat(
        data=signals_array,
        index=dates_index,
        columns=multi_index
        )

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
        if i > 30:
            optimized_returns: ArrayFloat = relative_sharpe_on_confidence_period(
                returns_array=raw_adjusted_returns_df.nparray
            )
            raw_adjusted_returns_df = DataFrameFloat(
                data=optimized_returns, 
                index=raw_adjusted_returns_df.dates, 
                columns=raw_adjusted_returns_df.columns
                )

        if i == 3:
            raw_adjusted_returns_df.dropna(axis=0, how='all', inplace=True)  # type: ignore
            sub_portfolio_rolling = DataFrameFloat(data=raw_adjusted_returns_df)
            raw_adjusted_returns_df.dropna(axis=0, how='any', inplace=True)  # type: ignore
            sub_portfolio_overall = DataFrameFloat(data=raw_adjusted_returns_df)

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