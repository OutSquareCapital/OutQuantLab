import pandas as pd
import numpy as np
import Metrics as mt

def calculate_cost_limit(
    raw_rolling_sharpe_df: pd.DataFrame, 
    net_rolling_sharpe_df: pd.DataFrame, 
    asset_names: list, 
    limit_treshold=0.05, 
    ma_window=250, 
    day_treshold = 60) -> pd.DataFrame:

    cost_validation_df = pd.DataFrame(
        0, 
        index=raw_rolling_sharpe_df.index, 
        columns=raw_rolling_sharpe_df.columns, 
        dtype=np.float32
        )

    for asset in asset_names:
        raw_sharpe_columns = [col for col in raw_rolling_sharpe_df.columns if asset in col]
        net_sharpe_columns = [col for col in net_rolling_sharpe_df.columns if asset in col]
        
        raw_sharpe = raw_rolling_sharpe_df[raw_sharpe_columns].values
        net_sharpe = net_rolling_sharpe_df[net_sharpe_columns].values
        
        sharpe_diff = (raw_sharpe + 100) - (net_sharpe + 100)
        
        ma_sharpe_diff = mt.rolling_mean(sharpe_diff, length=ma_window, min_length=1)
        
        positive_invalid_costs = (raw_sharpe > 0) & (ma_sharpe_diff > (raw_sharpe * limit_treshold))
        negative_invalid_costs = (raw_sharpe < 0) & (ma_sharpe_diff > ((raw_sharpe * limit_treshold)*-1))

        invalid_costs = positive_invalid_costs | negative_invalid_costs

        consecutive_days = np.zeros_like(invalid_costs, dtype=int)
        for i in range(1, len(invalid_costs)):
            consecutive_days[i] = np.where(invalid_costs[i], consecutive_days[i-1] + 1, 0)
        
        cost_validation_df[raw_sharpe_columns] = np.where(consecutive_days >= day_treshold, 0, 1)
    
    return cost_validation_df


def adjust_returns_by_impact(net_adjusted_returns_df: pd.DataFrame, cost_validation_df: pd.DataFrame) -> pd.DataFrame:

    adjusted_returns_df = net_adjusted_returns_df * cost_validation_df

    return adjusted_returns_df

def calculate_cost_adjusted_returns(
    raw_adjusted_returns_df: pd.DataFrame, 
    net_adjusted_returns_df: pd.DataFrame, 
    asset_names: list, 
    window_size: int = 250) -> pd.DataFrame:

    raw_rolling_sharpe_df = pd.DataFrame(
        mt.rolling_sharpe_ratios(raw_adjusted_returns_df, window_size, window_size),
        index=raw_adjusted_returns_df.index,
        columns=raw_adjusted_returns_df.columns)

    net_rolling_sharpe_df = pd.DataFrame(
        mt.rolling_sharpe_ratios(net_adjusted_returns_df, window_size, window_size),
        index=net_adjusted_returns_df.index,
        columns=net_adjusted_returns_df.columns)

    cost_validation_df = calculate_cost_limit(raw_rolling_sharpe_df, net_rolling_sharpe_df, asset_names)
    
    cost_adjusted_returns_df = adjust_returns_by_impact(net_adjusted_returns_df, cost_validation_df)
    
    return cost_adjusted_returns_df
