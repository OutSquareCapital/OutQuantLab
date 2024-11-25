import numpy as np
import pandas as pd
import Portfolio.Common as Common

def classify_assets(asset_list, portfolio):
    portfolios = {
        'Assets': {},
        'Ratios': {},
        'Ensembles': {}
    }

    def find_category_and_subcategory(asset, portfolio):

        for category, subcategories in portfolio.items():
            if isinstance(subcategories, dict):  # Check nested structure
                for subcategory, assets in subcategories.items():
                    if isinstance(assets, list) and asset in assets:
                        return category, subcategory
                    elif isinstance(assets, dict):  # Handle deeper nested levels
                        for deeper_subcategory, deeper_assets in assets.items():
                            if asset in deeper_assets:
                                return category, deeper_subcategory
            elif asset in subcategories:
                return category, None
        return None, None

    # Process each asset pair in the list
    for asset_pair in asset_list:
        if '+' in asset_pair:  # Ensemble case
            asset1, asset2 = asset_pair.split('+')
            portfolio_type = 'Ensembles'
        elif '-' in asset_pair:  # Ratio case
            asset1, asset2 = asset_pair.split('-')
            portfolio_type = 'Ratios'
        else:  # Individual asset case
            asset1 = asset_pair
            asset2 = None
            portfolio_type = 'Assets'
        
        # Find categories and subcategories for each asset
        category1, subcategory1 = find_category_and_subcategory(asset1, portfolio)
        category2, subcategory2 = find_category_and_subcategory(asset2, portfolio) if asset2 else (None, None)
        
        # Ignore the pair if any asset is not found in the portfolio
        if not category1 or (asset2 and not category2):
            continue
        
        # Determine the main category key
        if category1 == category2 or not category2:
            category_key = category1
        else:
            combined_category = sorted([category1, category2])
            category_key = f"{combined_category[0]} & {combined_category[1]}"
        
        # Determine the subcategory key
        if subcategory1 and subcategory2 and category1 == category2 and subcategory1 != subcategory2:
            subcategory_key = f"{subcategory1} & {subcategory2}"
        elif subcategory1 or subcategory2:
            subcategory_key = subcategory1 or subcategory2
        else:
            subcategory_key = 'General'

        # Add the pair to the appropriate portfolio
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
        if isinstance(value, list):  # Si c'est une liste d'actifs (feuille)
            num_assets = len(value)
            for asset in value:
                weighted_portfolio[asset] = parent_weight / total_items / num_assets
        elif isinstance(value, dict):  # Si c'est un sous-dictionnaire (sous-classe ou super-classe)
            sub_weights = generate_static_weights(value, parent_weight / total_items)
            weighted_portfolio.update(sub_weights)
    
    return weighted_portfolio

def generate_dynamic_weights(returns_df, base_weights):

    # Convertir le dictionnaire des poids de base en DataFrame aligné sur returns_df
    base_weights_df = pd.Series(base_weights).reindex(returns_df.columns)

    # Créer une matrice indiquant la disponibilité des actifs pour chaque date (NaN si indisponible)
    available_mask = returns_df.notna().astype(float)

    # Étendre les poids de base pour toutes les dates (en alignant avec l'index du DataFrame des rendements)
    base_weights_matrix = pd.DataFrame(np.tile(base_weights_df.values, (returns_df.shape[0], 1)),
                                    index=returns_df.index, columns=returns_df.columns, dtype=np.float32)

    # Appliquer le masque de disponibilité : les poids resteront NaN si les données de rendements sont NaN
    dynamic_weights = base_weights_matrix.where(available_mask == 1, np.nan)

    # Appliquer la renormalisation des poids
    adjusted_dynamic_weights = pd.DataFrame(Common.renormalize_weights(dynamic_weights, returns_df),
                                            index=dynamic_weights.index,
                                            columns=dynamic_weights.columns)

    return adjusted_dynamic_weights
