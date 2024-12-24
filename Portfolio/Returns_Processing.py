import bottleneck as bn
import numpy as np
import pandas as pd

def calculate_portfolio_returns(
    returns_df: pd.DataFrame,
    by_asset_cluster=False,
    by_asset_cluster_sub=False,
    by_asset=False,
    by_indic_cluster=False,
    by_indic_cluster_sub=False,
    by_indic=False,
    by_param=False
    ) -> pd.DataFrame:

    grouping_levels = []
    if by_asset_cluster:
        grouping_levels.append("AssetCluster")
    if by_asset_cluster_sub:
        grouping_levels.append("AssetSubCluster")
    if by_asset:
        grouping_levels.append("Asset")
    if by_indic_cluster:
        grouping_levels.append("IndicCluster")
    if by_indic_cluster_sub:
        grouping_levels.append("IndicSubCluster")
    if by_indic:
        grouping_levels.append("Indicator")
    if by_param:
        grouping_levels.append("Param")

    if grouping_levels:
        grouped = returns_df.T.groupby(level=grouping_levels, observed=True).mean().T

        return grouped

    return pd.DataFrame(
        bn.nanmean(returns_df.values, axis=1), 
        index=returns_df.index, 
        columns=['Portfolio'], 
        dtype=np.float32
        )

def aggregate_raw_returns(raw_adjusted_returns_df: pd.DataFrame):
    
    df_indic = calculate_portfolio_returns(
        raw_adjusted_returns_df.dropna(axis=0),
        by_asset_cluster=True,
        by_asset_cluster_sub=True,
        by_asset=True,
        by_indic_cluster=True,
        by_indic_cluster_sub=True,
        by_indic=True
    )

    df_indic_subcluster = calculate_portfolio_returns(
        df_indic,
        by_asset_cluster=True,
        by_asset_cluster_sub=True,
        by_asset=True,
        by_indic_cluster=True,
        by_indic_cluster_sub=True
    )

    df_indic_cluster = calculate_portfolio_returns(
        df_indic_subcluster,
        by_asset_cluster=True,
        by_asset_cluster_sub=True,
        by_asset=True,
        by_indic_cluster=True
    )

    df_asset = calculate_portfolio_returns(
        df_indic_cluster,
        by_asset_cluster=True,
        by_asset_cluster_sub=True,
        by_asset=True
    )

    df_asset_subcluster = calculate_portfolio_returns(
        df_asset,
        by_asset_cluster=True,
        by_asset_cluster_sub=True
    )

    df_asset_cluster = calculate_portfolio_returns(
        df_asset_subcluster,
        by_asset_cluster=True
    )

    df_global = calculate_portfolio_returns(
        df_asset_cluster
    )

    return df_global, df_asset