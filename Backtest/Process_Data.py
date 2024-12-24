import pandas as pd
import numpy as np
from Infrastructure import Fast_Tools as ft
from Files import PERCENTAGE_FACTOR
from collections.abc import Callable
import Metrics as mt

def load_prices(asset_names: list[str], file_path: str) -> pd.DataFrame:
    
    columns_to_load = ["Date"] + [name for name in asset_names]

    return pd.read_parquet(
        file_path,
        engine="pyarrow",
        columns=columns_to_load
    )
    
def calculate_volatility_adjusted_returns(
    pct_returns_array: np.ndarray, 
    hv_array: np.ndarray, 
    target_volatility: int = 15
    ) -> np.ndarray:

    vol_adj_position_size_shifted = ft.shift_array(target_volatility / hv_array)

    return pct_returns_array * vol_adj_position_size_shifted

def calculate_equity_curves(returns_array: np.ndarray) -> np.ndarray:

    temp_array = returns_array.copy()

    mask = np.isnan(temp_array)
    temp_array[mask] = 0

    cumulative_returns = np.cumprod(1 + temp_array, axis=0)

    cumulative_returns[mask] = np.nan

    return cumulative_returns * PERCENTAGE_FACTOR

def log_returns_np(prices_array: np.ndarray) -> np.ndarray:

    if prices_array.ndim == 1:
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0] = np.nan
        log_returns_array[1:] = np.log(prices_array[1:] / prices_array[:-1])
    else:
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0, :] = np.nan
        log_returns_array[1:, :] = np.log(prices_array[1:] / prices_array[:-1])
    
    return log_returns_array

def generate_multi_index_pandas(multi_index_tuples: list[tuple[str, str, str]]) -> pd.MultiIndex:
    
    multi_index_pandas = pd.MultiIndex.from_tuples(multi_index_tuples, names=["Asset", "Indicator", "Param"])
    multi_index_pandas = multi_index_pandas.set_levels(
        [
        pd.CategoricalIndex(multi_index_pandas.levels[0]),
        pd.CategoricalIndex(multi_index_pandas.levels[1]),
        multi_index_pandas.levels[2]
        ]
    )

    return multi_index_pandas

def generate_multi_index_process(
    indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]], 
    asset_names: list[str]
    ) -> pd.MultiIndex:
    
    multi_index_tuples: list[tuple[str, str, str]] = []
    
    for indicator_name, (_, _, params) in indicators_and_params.items():
        for param in params:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                multi_index_tuples.append((asset, indicator_name, param_str))

    return generate_multi_index_pandas(multi_index_tuples)

def process_data(
    data_prices_df: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    returns_df = data_prices_df.pct_change(fill_method=None)
    pct_returns_array = returns_df.to_numpy(dtype=np.float32)
    prices_array = ft.shift_array(calculate_equity_curves(pct_returns_array))
    log_returns_array = ft.shift_array(log_returns_np(prices_array))
    hv_array = mt.hv_composite(pct_returns_array)
    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(
        pct_returns_array, 
        hv_array
    )

    return prices_array, log_returns_array, volatility_adjusted_pct_returns