import bottleneck as bn
import numpy as np
import pandas as pd

def calculate_portfolio_returns(
    returns_df: pd.DataFrame, 
    by_asset=False,
    by_indic=False, 
    by_param=False
    ) -> pd.DataFrame:

    grouping_levels = []
    if by_asset:
        grouping_levels.append("Asset")
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
