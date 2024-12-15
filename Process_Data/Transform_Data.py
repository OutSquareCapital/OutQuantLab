import numexpr as ne
from scipy.stats import norm, rankdata
import pandas as pd
import numpy as np
from Infrastructure import Fast_Tools as ft
import Metrics as mt
from Files import PERCENTAGE_FACTOR
from collections.abc import Callable

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

    vol_adj_position_size_array = ne.evaluate('target_volatility / hv_array')

    vol_adj_position_size_shifted = ft.shift_array(vol_adj_position_size_array)

    return ne.evaluate('pct_returns_array * vol_adj_position_size_shifted')

def normalize_returns_distribution_rolling(
    pct_returns_df: pd.DataFrame, 
    window_size: int
    ) -> pd.DataFrame:
    
    normalized_returns = pd.DataFrame(
        index=pct_returns_df.index, 
        columns=pct_returns_df.columns, 
        dtype=np.float32)

    for end in range(window_size - 1, len(pct_returns_df)):
        window_df = pct_returns_df.iloc[end - window_size + 1 : end + 1]
        
        window_df_shifted = window_df.shift(1)
        window_df_shifted.fillna(0, inplace=True)
        returns = window_df_shifted.values
        
        mean_returns = np.mean(returns, axis=0)
        std_returns = np.std(returns, axis=0)
        
        ranks = np.apply_along_axis(lambda x: rankdata(x) / (len(x) + 1), axis=0, arr=returns)
        
        normalized_returns_window = norm.ppf(ranks)
        
        normalized_returns_window = normalized_returns_window * std_returns + mean_returns
        
        normalized_returns.iloc[end] = normalized_returns_window[-1]

    return normalized_returns

def equity_curves_calculs(returns_array: np.ndarray) -> np.ndarray:

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

def generate_multi_index_tuple(
    indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]], 
    asset_names: list[str]
    ) -> list[tuple[str, str, str]]:
    
    multi_index_tuples: list[tuple[str, str, str]] = []
    
    for indicator_name, (_, _, params) in indicators_and_params.items():
        for param in params:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                multi_index_tuples.append((asset, indicator_name, param_str))
    return multi_index_tuples

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
    
    index_tuples = generate_multi_index_tuple(indicators_and_params, asset_names)

    return generate_multi_index_pandas(index_tuples)

def get_total_return_streams_nb(
    indicators_and_params: dict[str, tuple[Callable, str, list[dict[str, int]]]], 
    asset_names: list[str]
    ) -> int:
    
    num_assets: int = len(asset_names)
    num_params: int = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
    
    return num_assets * num_params


def process_data(
    data_prices_df: pd.DataFrame
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    
    returns_df=data_prices_df.pct_change(fill_method=None)
    pct_returns_array = returns_df.to_numpy(dtype=np.float32)
    prices_array = equity_curves_calculs(pct_returns_array)
    log_returns_array = log_returns_np(prices_array)
    hv_array = mt.hv_composite(pct_returns_array)
    
    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(
        pct_returns_array, 
        hv_array
    )

    return prices_array, log_returns_array, volatility_adjusted_pct_returns

def initialize_data_array(
    prices_array: np.ndarray,
    log_returns_array: np.ndarray
    ) -> dict[str, np.ndarray]:

    shifted_log_returns = ft.shift_array(log_returns_array)
    shifted_prices = ft.shift_array(prices_array)

    return {
        'returns_array': shifted_log_returns,
        'prices_array': shifted_prices
    }

def initialize_signals_array(
    prices_array: np.ndarray,
    total_returns_streams: int
    ) -> np.ndarray:
    
    total_days = prices_array.shape[0]

    return np.full((total_days, total_returns_streams), np.nan, dtype=np.float32)


