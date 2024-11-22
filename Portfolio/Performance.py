import pandas as pd
import numpy as np
import Metrics as mt
from Infrastructure import Fast_Tools as ft
import numexpr as ne
import Portfolio.Common as Common

def relative_sharpe_on_confidence_period(returns_df:pd.DataFrame, sharpe_lookback:int, confidence_lookback = 2500):

    # Calcul du Sharpe ratio roulant
    sharpe_array = ft.process_in_blocks_parallel(
        returns_df.values, 
        block_size=10,
        func=mt.rolling_sharpe_ratios,
        length = sharpe_lookback,
        min_length = 125
    )

    # Moyenne roulante
    mean_sharpe_array = ft.process_in_blocks_parallel(
        sharpe_array, 
        block_size=10,
        func=mt.rolling_mean,
        length=20, min_length=1
    )

    # Calcul des jours non-NaN
    non_nan_counts = ft.process_in_blocks_parallel(
        mean_sharpe_array, 
        block_size=10,
        func=lambda x: np.cumsum(~np.isnan(x), axis=0, dtype=np.float32)
    )

    # Calcul de la médiane de chaque ligne de sharpe_array
    rolling_median_sharpe = np.nanmedian(mean_sharpe_array, axis=1)[:, np.newaxis]

    # Normalisation et ajustement des Sharpe ratios
    normalized_sharpes = ne.evaluate('(mean_sharpe_array - rolling_median_sharpe) * ((non_nan_counts / confidence_lookback)**0.5) + 1')

    # Clipping final
    clipped_sharpes = np.clip(normalized_sharpes, 0, None)

    return pd.DataFrame(clipped_sharpes, 
                        index=returns_df.index, 
                        columns= returns_df.columns,
                        dtype=np.float32
                        )

def calculate_weights(returns_array: np.ndarray, rolling_periods: list) -> np.ndarray:

    # Stocker les poids calculés pour chaque période glissante
    weights_array = np.zeros_like(returns_array, dtype=np.float32)

    # Boucle uniquement sur les périodes glissantes (les calculs par jour sont vectorisés)
    for rolling_period in rolling_periods:
        # Calcul de la moyenne glissante pour la période donnée en utilisant bottleneck.move_mean
        rolling_means = mt.rolling_mean(returns_array, length=rolling_period, min_length=1)

        # Calcul des poids : 1 si la moyenne est >= 0, sinon 0
        weights = (rolling_means >= 0).astype(np.float32)

        # Ajouter les poids à l'array principal (moyenne sur plusieurs périodes)
        weights_array += weights

    # Diviser par le nombre de périodes pour obtenir la moyenne des poids
    average_weights = weights_array / len(rolling_periods)

    return average_weights

def apply_returns_threshold(returns_array: np.ndarray, rolling_periods: list) -> np.ndarray:

    # Calcul des poids moyens avec la fonction optimisée en NumPy
    average_weights = calculate_weights(returns_array, rolling_periods)

    # Renormalisation des poids
    normalized_average_weights = Common.renormalize_weights(average_weights, returns_array)

    # Décalage des poids pour éviter le lookahead bias (décalage d'une ligne)
    normalized_shifted_weights = ft.shift_array(normalized_average_weights)

    # Mettre la première ligne à zéro pour éviter le lookahead sur le premier jour
    normalized_shifted_weights[0, :] = 0

    # Ajustement des rendements en multipliant par les poids décalés
    adjusted_returns = returns_array * normalized_shifted_weights

    return adjusted_returns

def apply_returns_threshold_generic(returns_df: pd.DataFrame, rolling_periods: list, by_class: bool = False) -> pd.DataFrame:

    # Convertir le DataFrame en tableau NumPy pour des calculs rapides
    returns_array = returns_df.to_numpy(dtype=np.float32)
    
    # Extraire les noms d'assets et potentiellement des classes
    columns = returns_df.columns
    if by_class:
        # Si on traite par classe, on divise les colonnes en 'Asset_Class'
        assets_classes = np.array([col.split('_')[:2] for col in columns])  # ex: [['asset1', 'class1'], ['asset1', 'class2']]
        assets = assets_classes[:, 0]  # Sélectionner les noms des assets
    else:
        # Sinon on ne s'intéresse qu'aux assets
        assets = np.array([col.split('_')[0] for col in columns])  # ex: ['asset1', 'asset2', ...]

    # Identifier les différents assets
    unique_assets = np.unique(assets)
    
    # Initialiser une matrice pour stocker les rendements ajustés
    adjusted_returns_array = np.zeros_like(returns_array)
    
    # Boucler sur chaque asset
    for asset in unique_assets:
        # Mask pour sélectionner toutes les colonnes liées à cet asset
        asset_mask = (assets == asset)
        asset_returns = returns_array[:, asset_mask]

        if by_class:
            # Identifier les classes dans cet asset
            asset_classes = assets_classes[asset_mask][:, 1]  # Sélectionner les classes de cet asset
            unique_asset_classes = np.unique(asset_classes)

            # Boucler sur chaque classe de l'asset
            for class_name in unique_asset_classes:
                # Mask pour sélectionner les colonnes de la classe spécifique
                class_mask = (asset_classes == class_name)
                class_returns = asset_returns[:, class_mask]

                # Appliquer la nouvelle version NumPy de apply_returns_threshold
                adjusted_class_returns = apply_returns_threshold(class_returns, rolling_periods)

                # Trouver les indices des colonnes originales dans adjusted_returns_array correspondant aux colonnes de cette classe
                global_class_mask = np.where(asset_mask)[0][class_mask]
                
                # Remettre les résultats dans la matrice finale uniquement sur ces colonnes
                adjusted_returns_array[:, global_class_mask] = adjusted_class_returns

        else:
            # Si on ne gère que les assets
            adjusted_asset_returns = apply_returns_threshold(asset_returns, rolling_periods)

            # Remettre les résultats dans la matrice finale
            adjusted_returns_array[:, asset_mask] = adjusted_asset_returns
    
    # Conversion du tableau ajusté en DataFrame
    adjusted_returns_df = pd.DataFrame(adjusted_returns_array, 
                                        index=returns_df.index, 
                                        columns=returns_df.columns, 
                                        dtype=np.float32
                                        )
    
    return adjusted_returns_df