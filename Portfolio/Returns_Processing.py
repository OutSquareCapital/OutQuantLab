import bottleneck as bn
import numpy as np
import pandas as pd

def generate_recursive_means(returns_df: pd.DataFrame, asset_tree):
    
    group_means = [] 
    for key, value in asset_tree.items():
        if isinstance(value, dict):
            sub_group_mean = generate_recursive_means(returns_df, value)
            group_means.append(sub_group_mean)
        
        elif isinstance(value, list):
            sub_group_mean = pd.Series(
                bn.nanmean(returns_df[value], axis=1), 
                index=returns_df.index)
            group_means.append(sub_group_mean)

    if group_means: 
        final_mean = pd.concat(group_means, axis=1).mean(axis=1)
        return pd.DataFrame(
            final_mean, 
            columns=['PortfolioReturns'], 
            dtype=np.float32)
    else:
        return pd.DataFrame(
            np.nan, 
            index=returns_df.index, 
            columns=['PortfolioReturns'], 
            dtype=np.float32
            )

def generate_recursive_strategy_means(returns_df: pd.DataFrame, strategy_tree):
    strategy_means = {}

    for key, value in strategy_tree.items():
        if isinstance(value, dict):
            sub_strategy_means = generate_recursive_strategy_means(returns_df, value)
            for asset, sub_mean in sub_strategy_means.items():
                if asset in strategy_means:
                    strategy_means[asset].append(sub_mean)
                else:
                    strategy_means[asset] = [sub_mean]
        elif isinstance(value, list):
            for asset in returns_df.columns.str.split('_').str[0].unique():
                matching_columns = [
                    col for col in returns_df.columns 
                    if col.startswith(asset) and any(
                        strategy in col for strategy in value)
                    ]
                sub_strategy_mean = pd.Series(
                    bn.nanmean(returns_df[matching_columns], axis=1), 
                    index=returns_df.index, 
                    name=asset, 
                    dtype=np.float32
                )
                if asset in strategy_means:
                    strategy_means[asset].append(sub_strategy_mean)
                else:
                    strategy_means[asset] = [sub_strategy_mean]

    final_means = {asset: pd.concat(means, axis=1).mean(axis=1) for asset, means in strategy_means.items()}

    return pd.DataFrame(final_means, dtype=np.float32)


def generate_recursive_cluster_means(
    returns_df: pd.DataFrame, 
    cluster_tree, 
    by_cluster=False
    ) -> pd.DataFrame:

    group_means = {}

    for cluster_key, cluster_value in cluster_tree.items():
        if isinstance(cluster_value, dict):

            if not by_cluster:
                sub_group_mean = generate_recursive_cluster_means(returns_df, cluster_value, by_cluster)
                group_means[cluster_key] = sub_group_mean
            else:
                matching_columns = []
                for sub_key, sub_items in cluster_value.items():
                    matching_columns += [col for col in returns_df.columns if any(str(item) in col for item in sub_items)]
                
                if matching_columns:
                    cluster_mean = pd.Series(
                        bn.nanmean(returns_df[matching_columns], axis=1), 
                        index=returns_df.index, 
                        name=f'Cluster_{cluster_key}')
                    group_means[cluster_key] = cluster_mean
        
        elif isinstance(cluster_value, list):
            matching_columns = [col for col in returns_df.columns if any(item in col for item in cluster_value)]
            if matching_columns:
                sub_group_mean = pd.Series(
                    bn.nanmean(returns_df[matching_columns], 
                    axis=1), 
                    index=returns_df.index, 
                    name=f'Cluster_{cluster_key}')
                group_means[cluster_key] = sub_group_mean

    if by_cluster and group_means:
        return pd.DataFrame(
                group_means, 
                dtype=np.float32)

    if group_means:
        final_mean = pd.concat(group_means.values(), axis=1).mean(axis=1)
        return pd.DataFrame(
            final_mean, 
            columns=['Cluster_Mean'], 
            dtype=np.float32)

    return pd.DataFrame(
        np.nan, 
        index=returns_df.index, 
        columns=['Cluster_Mean'], 
        dtype=np.float32)

def calculate_daily_average_returns(
    returns_df: pd.DataFrame, 
    global_avg=False, 
    by_asset=False,
    by_method=False, 
    by_param=False,
    common_start_date=False
    ) -> pd.DataFrame:

    if common_start_date:
        returns_df = returns_df.dropna(how='any')

    if global_avg:
        daily_averages = bn.nanmean(returns_df.values, axis=1)
        return pd.DataFrame(daily_averages, 
                            index=returns_df.index, 
                            columns=['Portfolio'], 
                            dtype=np.float32)

    grouping_levels = []
    if by_asset:
        grouping_levels.append("Asset")
    if by_method:
        grouping_levels.append("Indicator")
    if by_param:
        grouping_levels.append("Param")

    if grouping_levels:
        grouped = returns_df.T.groupby(level=grouping_levels, observed=True).mean().T

        return grouped

    return returns_df
