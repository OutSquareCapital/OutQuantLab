import pandas as pd
import numpy as np
from .Backtest_Process import transform_signals_into_returns
from collections.abc import Callable

def data_arrays_to_dataframe(
    raw_adjusted_returns_array: np.ndarray, 
    dates_index: pd.Index, 
    indicators_and_params: dict, 
    asset_names: list
    ) -> pd.DataFrame:

    multiindex_tuples = []
    for indicator_name, (_, _, params) in indicators_and_params.items():
        for param in params:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                multiindex_tuples.append((asset, indicator_name, param_str))

    multiindex = pd.MultiIndex.from_tuples(multiindex_tuples, names=["Asset", "Indicator", "Param"])
    multiindex = multiindex.set_levels(
        [
        pd.CategoricalIndex(multiindex.levels[0]),
        pd.CategoricalIndex(multiindex.levels[1]),
        multiindex.levels[2]]
    )

    return pd.DataFrame(raw_adjusted_returns_array, 
                        index=dates_index, 
                        columns=multiindex, 
                        dtype=np.float32)

def process_backtest(prices_array: np.ndarray, 
                    log_returns_array: np.ndarray,
                    volatility_adjusted_pct_returns_array: np.ndarray,
                    asset_names: list,
                    dates_index: pd.Index,
                    indicators_and_params: dict,
                    progress_callback: Callable
                    ) -> pd.DataFrame:

    raw_adjusted_returns_array = transform_signals_into_returns(prices_array,
                                                                log_returns_array,
                                                                volatility_adjusted_pct_returns_array,
                                                                asset_names,
                                                                indicators_and_params,
                                                                progress_callback)

    return data_arrays_to_dataframe(raw_adjusted_returns_array, 
                                    dates_index, 
                                    indicators_and_params, 
                                    asset_names)