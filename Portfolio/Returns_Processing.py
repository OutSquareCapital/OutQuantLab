from Metrics import calculate_overall_mean
from Utilitary import DataFrameFloat

def calculate_portfolio_returns(
    returns_df: DataFrameFloat,
    by_asset_cluster: bool = False,
    by_asset_cluster_sub: bool = False,
    by_asset: bool = False,
    by_indic_cluster: bool = False,
    by_indic_cluster_sub: bool = False,
    by_indic: bool = False,
    by_param: bool = False
    ) -> DataFrameFloat:

    grouping_levels:list[str] = []
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

        return DataFrameFloat(grouped)

    global_portfolio = calculate_overall_mean(returns_df.nparray, axis=1)
    return DataFrameFloat(
        data=global_portfolio,
        index=returns_df.dates,
        columns=['Portfolio']
        )

def aggregate_raw_returns(raw_adjusted_returns_df: DataFrameFloat, all_history: bool = False) -> tuple[DataFrameFloat, DataFrameFloat]:
    
    if not all_history:
        raw_adjusted_returns_df= raw_adjusted_returns_df.dropna(axis=0) # type: ignore
    
    df_indic = calculate_portfolio_returns(
        raw_adjusted_returns_df,
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