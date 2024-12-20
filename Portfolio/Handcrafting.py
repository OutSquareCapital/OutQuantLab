import numpy as np
import pandas as pd
import Portfolio.Common as Common

def classify_assets(asset_list: list[str], portfolio):
    portfolios = {
        'Assets': {},
        'Ratios': {},
        'Ensembles': {}
    }

    def find_category_and_subcategory(asset, portfolio):

        for category, subcategories in portfolio.items():
            if isinstance(subcategories, dict):
                for subcategory, assets in subcategories.items():
                    if isinstance(assets, list) and asset in assets:
                        return category, subcategory
                    elif isinstance(assets, dict):
                        for deeper_subcategory, deeper_assets in assets.items():
                            if asset in deeper_assets:
                                return category, deeper_subcategory
            elif asset in subcategories:
                return category, None
        return None, None

    for asset_pair in asset_list:
        if '+' in asset_pair:
            asset1, asset2 = asset_pair.split('+')
            portfolio_type = 'Ensembles'
        elif '-' in asset_pair:
            asset1, asset2 = asset_pair.split('-')
            portfolio_type = 'Ratios'
        else:
            asset1 = asset_pair
            asset2 = None
            portfolio_type = 'Assets'
        
        category1, subcategory1 = find_category_and_subcategory(asset1, portfolio)
        category2, subcategory2 = find_category_and_subcategory(asset2, portfolio) if asset2 else (None, None)
        
        if not category1 or (asset2 and not category2):
            continue
        
        if category1 == category2 or not category2:
            category_key = category1
        else:
            combined_category = sorted([category1, category2])
            category_key = f"{combined_category[0]} & {combined_category[1]}"
        
        if subcategory1 and subcategory2 and category1 == category2 and subcategory1 != subcategory2:
            subcategory_key = f"{subcategory1} & {subcategory2}"
        elif subcategory1 or subcategory2:
            subcategory_key = subcategory1 or subcategory2
        else:
            subcategory_key = 'General'

        if category_key not in portfolios[portfolio_type]:
            portfolios[portfolio_type][category_key] = {}

        if subcategory_key not in portfolios[portfolio_type][category_key]:
            portfolios[portfolio_type][category_key][subcategory_key] = []
        
        portfolios[portfolio_type][category_key][subcategory_key].append(asset_pair)
    
    return portfolios

def generate_static_weights(portfolio, parent_weight=1.0):

    total_items = len(portfolio)
    weighted_portfolio = {}
    
    for key, value in portfolio.items():
        if isinstance(value, list):
            num_assets = len(value)
            for asset in value:
                weighted_portfolio[asset] = parent_weight / total_items / num_assets
        elif isinstance(value, dict):
            sub_weights = generate_static_weights(value, parent_weight / total_items)
            weighted_portfolio.update(sub_weights)
    
    return weighted_portfolio

def generate_dynamic_weights(returns_df: pd.DataFrame, base_weights):

    base_weights_df = pd.Series(base_weights).reindex(returns_df.columns)

    available_mask = returns_df.notna().astype(float)

    base_weights_matrix = pd.DataFrame(
        np.tile(base_weights_df.values, (returns_df.shape[0], 1)),
        index=returns_df.index, 
        columns=returns_df.columns, 
        dtype=np.float32)

    dynamic_weights = base_weights_matrix.where(available_mask == 1, np.nan)

    return pd.DataFrame(
        Common.renormalize_weights(dynamic_weights, returns_df),
        index=dynamic_weights.index,
        columns=dynamic_weights.columns)
