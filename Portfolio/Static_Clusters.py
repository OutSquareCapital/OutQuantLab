import numpy as np
import pandas as pd
import bottleneck as bn
import Portfolio.Common as Common

def classify_assets(asset_list, portfolio):
    portfolios = {
        'Assets': {},
        'Ratios': {},
        'Ensembles': {}
    }

    def find_category_and_subcategory(asset, portfolio):
        """
        Helper function to find the main category and subcategory of a single asset.
        """
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
    """
    Génère un dictionnaire des poids égaux pour chaque actif dans le portefeuille, 
    en gérant une hiérarchie flexible.
    """
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
    """
    Génère un DataFrame des poids dynamiques en fonction des actifs disponibles pour chaque période,
    et ajuste les poids en fonction du nombre d'actifs disponibles pour éviter la perte de volatilité.
    
    Args:
        returns_df (pd.DataFrame): DataFrame des rendements des actifs.
        base_weights (dict): Dictionnaire des poids de base pour chaque actif.

    Returns:
        pd.DataFrame: DataFrame des poids dynamiques ajustés.
    """
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

def generate_recursive_means(returns_df, asset_tree):
    """
    Génère les moyennes des rendements de manière récursive en descendant dans l'arbre d'actifs, puis en remontant 
    pour calculer les moyennes à chaque niveau (feuilles -> sous-groupes -> groupes -> niveau global).

    Args:
        returns_df (pd.DataFrame): DataFrame des rendements des actifs.
        asset_tree (dict): Dictionnaire imbriqué représentant la structure des actifs.

    Returns:
        pd.Series: Moyenne des rendements à chaque niveau du dictionnaire.
    """
    
    group_means = []  # Liste pour stocker les moyennes calculées à chaque niveau

    # Parcours récursif de l'arbre des actifs
    for key, value in asset_tree.items():
        if isinstance(value, dict):
            # Si c'est un sous-groupe, on applique la récursion pour obtenir les moyennes des sous-groupes
            sub_group_mean = generate_recursive_means(returns_df, value)
            group_means.append(sub_group_mean)
        
        elif isinstance(value, list):
            # Si c'est une liste d'actifs, on calcule la moyenne des rendements pour ces actifs
            sub_group_mean = pd.Series(bn.nanmean(returns_df[value], axis=1), index=returns_df.index)
            group_means.append(sub_group_mean)

    # Si on a des moyennes pour ce groupe, on calcule la moyenne finale à ce niveau
    if group_means:
        # Concaténer les sous-groupes ou actifs pour calculer la moyenne au niveau supérieur
        final_mean = pd.concat(group_means, axis=1).mean(axis=1)
        return pd.DataFrame(final_mean, columns=['PortfolioReturns'], dtype=np.float32)
    else:
        # Si aucune donnée n'est disponible, retourner un DataFrame vide avec des NaN
        return pd.DataFrame(np.nan, index=returns_df.index, columns=['PortfolioReturns'], dtype=np.float32)

def generate_recursive_strategy_means(returns_df, strategy_tree):
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
                matching_columns = [col for col in returns_df.columns 
                                    if col.startswith(asset) and any(strategy in col for strategy in value)]
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


def calculate_daily_average_returns(returns_df: pd.DataFrame, 
                                    global_avg=False, 
                                    by_asset=False, 
                                    by_class=False, 
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
                            columns=['Daily_Average_Returns'], 
                            dtype=np.float32)

    grouping_keys = []
    if by_asset:
        grouping_keys.append(0)
    if by_class:
        grouping_keys.append(1)
    if by_method:
        grouping_keys.append(2)
    if by_param:
        grouping_keys.append(3)


    
    if grouping_keys:
        keys = np.array([tuple(col.split('_')[pos] for pos in grouping_keys) for col in returns_df.columns])
        unique_keys, inverse_indices = np.unique(keys, return_inverse=True, axis=0)

        grouped_averages = {}
        for i, unique_key in enumerate(unique_keys):
            mask = (inverse_indices == i)
            selected_columns = returns_df.columns[mask]
            mean_values = bn.nanmean(returns_df[selected_columns].values, axis=1)
            grouped_averages['_'.join(unique_key)] = mean_values

        return pd.DataFrame(grouped_averages, 
                            index=returns_df.index, 
                            dtype=np.float32)

    return returns_df
