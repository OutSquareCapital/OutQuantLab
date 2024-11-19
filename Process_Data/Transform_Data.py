import numexpr as ne
from scipy.stats import norm, rankdata
import pandas as pd
import numpy as np
from Infrastructure import Fast_Tools as ft
from typing import List, Tuple
import Metrics as mt
from itertools import combinations


def calculate_volatility_adjusted_returns(
    pct_returns_array: np.ndarray, 
    hv_array: np.ndarray, 
    target_volatility: int = 15
    ) -> np.ndarray:


    vol_adj_position_size_array = ne.evaluate('target_volatility / hv_array')

    vol_adj_position_size_shifted = ft.shift_array(vol_adj_position_size_array)

    return ne.evaluate('pct_returns_array * vol_adj_position_size_shifted')

def normalize_returns_distribution_rolling(pct_returns_df: pd.DataFrame, 
                                            window_size: int) -> pd.DataFrame:
    
    normalized_returns = pd.DataFrame(index=pct_returns_df.index, 
                                        columns=pct_returns_df.columns, 
                                        dtype=np.float32)
    
    for end in range(window_size - 1, len(pct_returns_df)):
        # Utiliser une fenêtre roulante qui prend en compte 'window_size' périodes
        window_df = pct_returns_df.iloc[end - window_size + 1 : end + 1]
        
        # Décaler les données pour éviter le lookahead bias
        window_df_shifted = window_df.shift(1)
        window_df_shifted.fillna(0, inplace=True)
        # Récupérer les rendements avec NaN remplacés
        returns = window_df_shifted.values
        
        # Sauvegarder la moyenne et l'écart-type des rendements
        mean_returns = np.mean(returns, axis=0)
        std_returns = np.std(returns, axis=0)
        
        # Ranker les rendements (préservation de l'ordre)
        ranks = np.apply_along_axis(lambda x: rankdata(x) / (len(x) + 1), axis=0, arr=returns)
        
        # Transformation inverse normale pour obtenir des rendements à distribution normale
        normalized_returns_window = norm.ppf(ranks)
        
        # Ajuster pour conserver la moyenne et l'écart-type des rendements originaux
        normalized_returns_window = normalized_returns_window * std_returns + mean_returns
        
        # Stocker les résultats normalisés dans le DataFrame
        normalized_returns.iloc[end] = normalized_returns_window[-1]

    return normalized_returns

def equity_curves_calculs(daily_returns: pd.DataFrame , initial_equity: int =100) -> pd.DataFrame:

    equity_curves = (1 + daily_returns).cumprod() * initial_equity

    # Mettre à jour les dernières valeurs NaN dans equity_curves afin de correspondre à initial equity
    for asset in equity_curves.columns:
        na_positions = equity_curves[asset].isna()
        if na_positions.any():
            na_indices = equity_curves.index[na_positions]
            last_na_index = na_indices[-1]
            equity_curves.loc[last_na_index, asset] = initial_equity
    
    return equity_curves

def pct_returns_np(prices_array: np.ndarray) -> np.ndarray:

    # Vérifie si l'array est 1D ou 2D
    if prices_array.ndim == 1:
        # Si c'est 1D, initialisation d'un array pour les rendements
        pct_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        pct_returns_array[0] = np.nan  # Première ligne doit être NaN
        pct_returns_array[1:] = np.diff(prices_array) / prices_array[:-1]  # Calcul des rendements simples
    else:
        # Si c'est 2D, garde le comportement d'origine
        pct_returns_array = np.empty_like(prices_array, dtype=np.float32)
        pct_returns_array[0, :] = np.nan  # Première ligne doit être NaN
        pct_returns_array[1:, :] = np.diff(prices_array, axis=0) / prices_array[:-1, :]  # Calcul des rendements simples
    
    return pct_returns_array

def log_returns_df(prices_df: pd.DataFrame) -> pd.DataFrame:

    return np.log(prices_df / prices_df.shift(1))

def log_returns_np(prices_array: np.ndarray) -> np.ndarray:

    # Vérifie si l'array est 1D ou 2D
    if prices_array.ndim == 1:
        # Si c'est 1D, initialisation d'un array pour les rendements
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0] = np.nan  # La première valeur doit être NaN
        log_returns_array[1:] = np.log(prices_array[1:] / prices_array[:-1])  # Calcul des rendements log
    else:
        # Si c'est 2D, garde le comportement d'origine
        log_returns_array = np.empty(prices_array.shape, dtype=np.float32)
        log_returns_array[0, :] = np.nan  # Première ligne doit être NaN
        log_returns_array[1:, :] = np.log(prices_array[1:] / prices_array[:-1])  # Calcul des rendements log
    
    return log_returns_array

def extract_data_from_pct_returns(pct_returns_df: pd.DataFrame, initial_equity:int) -> Tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray, List[str]]:

    # Création de l'array des pct returns
    pct_returns_array = pct_returns_df.to_numpy(dtype=np.float32)

    # Création du DataFrame des prix avec des NaN
    prices_df = equity_curves_calculs(pct_returns_df, initial_equity)

    # Conversion en array
    prices_array = prices_df.to_numpy(dtype=np.float32)
    
    # Calcul des rendements log
    log_returns_array = log_returns_np(prices_array)
    hv_array = mt.hv_composite(pct_returns_array)

    log_returns_df = pd.DataFrame(log_returns_array, 
                                    index=prices_df.index, 
                                    columns=prices_df.columns,
                                    dtype=np.float32)


    # Liste des noms des actifs
    asset_names = list(prices_df.columns)
    
    return prices_df, prices_array, pct_returns_df, pct_returns_array, log_returns_df, log_returns_array, hv_array, asset_names

def extract_data_from_prices(prices_df: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray, pd.DataFrame, np.ndarray, List[str]]:

    # Conversion du DataFrame de prix en array
    prices_array = prices_df.to_numpy(dtype=np.float32)

    # Calcul des rendements simples
    pct_returns_array = pct_returns_np(prices_array)

    pct_returns_df = pd.DataFrame(pct_returns_array, index=prices_df.index, columns=prices_df.columns, dtype=np.float32)

    # Calcul des rendements log
    log_returns_array = log_returns_np(prices_array)
    log_returns_df = pd.DataFrame(log_returns_array, prices_df.index, prices_df.columns, dtype=np.float32)
    
    # Liste des noms des actifs
    asset_names = list(prices_df.columns)

    return prices_df, prices_array, pct_returns_df, pct_returns_array, log_returns_df, log_returns_array, asset_names

def calculate_ratios_returns(returns_df: pd.DataFrame, asset_names: list) -> pd.DataFrame:

    # Création d'une liste pour stocker les DataFrames de chaque paire
    pair_returns_list = []
    
    # Calcul des ratios de rendements pour toutes les paires
    for asset1, asset2 in combinations(asset_names, 2):
        pair_name = f"{asset1}-{asset2}"
        if asset1 in returns_df.columns and asset2 in returns_df.columns:
            # Soustraction des rendements des deux actifs
            pair_returns = returns_df[asset1] - returns_df[asset2]
            pair_returns_list.append(pair_returns.rename(f"{asset1}-{asset2}"))
    
    # Concaténation des résultats dans un seul DataFrame
    ratios_returns_df = pd.concat(pair_returns_list, axis=1)
    
    return ratios_returns_df

def calculate_ensembles_returns(returns_df: pd.DataFrame, asset_names: list, combination_size: int = 2) -> pd.DataFrame:

    # Création d'une liste pour stocker les rendements combinés
    ensembles_returns_list = []
    comb_names = []

    # Calcul des rendements combinés pour toutes les combinaisons d'actifs de la taille spécifiée
    for assets_comb in combinations(asset_names, combination_size):
        comb_name = '+'.join(assets_comb)

        if all(asset in returns_df.columns for asset in assets_comb):
            # Moyenne des rendements ajustés pour les actifs de la combinaison
            comb_returns = returns_df[list(assets_comb)].mean(axis=1, skipna=False)
            ensembles_returns_list.append(comb_returns.rename(comb_name))
            comb_names.append(comb_name)

    # Concaténation des résultats dans un seul DataFrame
    ensembles_returns_df = pd.concat(ensembles_returns_list, axis=1)

    return ensembles_returns_df

def adjust_prices_for_inversion(data_prices_df: pd.DataFrame, columns_list: list) -> pd.DataFrame:
    """
    Inverse les rendements pour les colonnes spécifiées, calcule les courbes d'équité à partir des rendements inversés,
    et remplace les colonnes originales dans le DataFrame par les nouveaux prix calculés.

    Args:
        data_prices_df (pd.DataFrame): Le DataFrame contenant les prix historiques.
        colonnes (list): Liste des noms de colonnes à inverser et à recalculer.
        initial_equity (float): Valeur initiale pour calculer la courbe d'équité. Par défaut 1.0.

    Returns:
        pd.DataFrame: Le DataFrame mis à jour avec les colonnes inversées recalculées.
    """
    for column in columns_list:
        # Calcul des rendements pour la colonne spécifiée
        returns = data_prices_df[column].pct_change()
        
        # Inverser les rendements
        inverted_returns = returns * -1
        
        # Convertir en DataFrame pour le traitement dans la fonction equity_curves_calculs
        inverted_returns_df = inverted_returns.to_frame(name=column)
        
        # Calculer la courbe d'équité à partir des rendements inversés
        inverted_price = equity_curves_calculs(inverted_returns_df)
        
        # Remplacer la colonne originale dans le DataFrame par les nouveaux prix
        data_prices_df[column] = inverted_price.squeeze()
    
    return data_prices_df