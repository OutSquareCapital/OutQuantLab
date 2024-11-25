import bottleneck as bn
import numpy as np
import pandas as pd

def generate_recursive_means(returns_df, asset_tree):
    
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

def generate_recursive_cluster_means(returns_df, cluster_tree, by_cluster=False):

    group_means = {}  # Dictionnaire pour stocker les moyennes calculées à chaque niveau

    # Parcours récursif de l'arbre des clusters
    for cluster_key, cluster_value in cluster_tree.items():
        if isinstance(cluster_value, dict):
            # Si c'est un sous-cluster, appliquer la récursion pour obtenir les moyennes des sous-groupes
            if not by_cluster:
                sub_group_mean = generate_recursive_cluster_means(returns_df, cluster_value, by_cluster)
                group_means[cluster_key] = sub_group_mean
            else:
                # Si by_cluster est True, on ne descend pas plus bas, et on passe directement à ce niveau
                matching_columns = []
                for sub_key, sub_items in cluster_value.items():
                    # Filtrer les colonnes qui correspondent aux items du sous-cluster
                    matching_columns += [col for col in returns_df.columns if any(str(item) in col for item in sub_items)]
                
                if matching_columns:
                    # Calculer la moyenne des colonnes correspondantes pour ce cluster spécifique
                    cluster_mean = pd.Series(bn.nanmean(returns_df[matching_columns], axis=1), index=returns_df.index, name=f'Cluster_{cluster_key}')
                    group_means[cluster_key] = cluster_mean
        
        elif isinstance(cluster_value, list):
            # Si c'est une liste d'actifs (ou de stratégies), calculer la moyenne des rendements pour ces actifs
            matching_columns = [col for col in returns_df.columns if any(item in col for item in cluster_value)]
            if matching_columns:
                sub_group_mean = pd.Series(bn.nanmean(returns_df[matching_columns], axis=1), index=returns_df.index, name=f'Cluster_{cluster_key}')
                group_means[cluster_key] = sub_group_mean

    # Si by_cluster est True, on retourne directement les moyennes des plus hauts clusters
    if by_cluster and group_means:
        return pd.DataFrame(group_means, dtype=np.float32)
    
    # Si on n'a pas encore remonté, on calcule la moyenne finale en remontant à tous les niveaux
    if group_means:
        final_mean = pd.concat(group_means.values(), axis=1).mean(axis=1)
        return pd.DataFrame(final_mean, columns=['Cluster_Mean'], dtype=np.float32)
    
    # Si aucune donnée n'est disponible, retourner un DataFrame vide avec des NaN
    return pd.DataFrame(np.nan, index=returns_df.index, columns=['Cluster_Mean'], dtype=np.float32)
