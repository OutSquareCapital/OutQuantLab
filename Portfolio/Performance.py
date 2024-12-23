import pandas as pd
import numpy as np
import Metrics as mt
from Infrastructure import Fast_Tools as ft
import numexpr as ne
from .Common import renormalize_weights

def relative_sharpe_on_confidence_period(returns_df:pd.DataFrame, sharpe_lookback:int, confidence_lookback = 2500):

    sharpe_array = ft.process_in_blocks_parallel(
        returns_df.values, 
        block_size=10,
        func=mt.rolling_sharpe_ratios,
        length = sharpe_lookback,
        min_length = 125
    )

    mean_sharpe_array = ft.process_in_blocks_parallel(
        sharpe_array, 
        block_size=10,
        func=mt.rolling_mean,
        length=20, min_length=1
    )

    non_nan_counts = ft.process_in_blocks_parallel(
        mean_sharpe_array, 
        block_size=10,
        func=lambda x: np.cumsum(~np.isnan(x), axis=0, dtype=np.float32)
    )

    rolling_median_sharpe = np.nanmedian(mean_sharpe_array, axis=1)[:, np.newaxis]

    normalized_sharpes = ne.evaluate('(mean_sharpe_array - rolling_median_sharpe) * ((non_nan_counts / confidence_lookback)**0.5) + 1')

    clipped_sharpes = np.clip(normalized_sharpes, 0, None)

    return pd.DataFrame(
        clipped_sharpes, 
        index=returns_df.index, 
        columns= returns_df.columns,
        dtype=np.float32
        )

def calculate_weights(returns_array: np.ndarray, rolling_periods: list) -> np.ndarray:

    weights_array = np.zeros_like(returns_array, dtype=np.float32)

    for rolling_period in rolling_periods:
        rolling_means = mt.rolling_mean(returns_array, length=rolling_period, min_length=1)

        weights = (rolling_means >= 0).astype(np.float32)

        weights_array += weights

    average_weights = weights_array / len(rolling_periods)

    return average_weights

def apply_returns_threshold(returns_array: np.ndarray, rolling_periods: list) -> np.ndarray:

    average_weights = calculate_weights(returns_array, rolling_periods)

    normalized_average_weights = renormalize_weights(average_weights, returns_array)

    normalized_shifted_weights = ft.shift_array(normalized_average_weights)

    normalized_shifted_weights[0, :] = 0

    adjusted_returns = returns_array * normalized_shifted_weights

    return adjusted_returns

def apply_returns_threshold_generic(returns_df: pd.DataFrame, rolling_periods: list, by_class: bool = False) -> pd.DataFrame:

    returns_array = returns_df.to_numpy(dtype=np.float32)
    
    columns = returns_df.columns
    if by_class:
        assets_classes = np.array([col.split('_')[:2] for col in columns])
        assets = assets_classes[:, 0]
    else:
        assets = np.array([col.split('_')[0] for col in columns])

    unique_assets = np.unique(assets)
    
    adjusted_returns_array = np.zeros_like(returns_array)
    
    for asset in unique_assets:
        asset_mask = (assets == asset)
        asset_returns = returns_array[:, asset_mask]

        if by_class:
            asset_classes = assets_classes[asset_mask][:, 1]
            unique_asset_classes = np.unique(asset_classes)

            for class_name in unique_asset_classes:
                class_mask = (asset_classes == class_name)
                class_returns = asset_returns[:, class_mask]

                adjusted_class_returns = apply_returns_threshold(class_returns, rolling_periods)

                global_class_mask = np.where(asset_mask)[0][class_mask]
                
                adjusted_returns_array[:, global_class_mask] = adjusted_class_returns

        else:
            adjusted_asset_returns = apply_returns_threshold(asset_returns, rolling_periods)

            adjusted_returns_array[:, asset_mask] = adjusted_asset_returns
    
    adjusted_returns_df = pd.DataFrame(
        adjusted_returns_array, 
        index=returns_df.index, 
        columns=returns_df.columns, 
        dtype=np.float32
        )

    return adjusted_returns_df