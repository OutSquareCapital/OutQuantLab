import numexpr as ne
from scipy.stats import norm, rankdata
import pandas as pd
import numpy as np
from Infrastructure import Fast_Tools as ft
from typing import List, Tuple
import Metrics as mt
from itertools import combinations
import Config

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

def equity_curves_calculs(daily_returns_array: np.ndarray) -> np.ndarray:
    mask = np.isnan(daily_returns_array)
    daily_returns_array[mask] = 0
    cumulative_returns = np.cumprod(1 + daily_returns_array, axis=0)
    cumulative_returns[mask] = np.nan
    return cumulative_returns * Config.PERCENTAGE_FACTOR

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

def extract_data_from_pct_returns(pct_returns_df: pd.DataFrame) -> Tuple[np.ndarray, 
                                                                        np.ndarray, 
                                                                        np.ndarray,
                                                                        List[str],
                                                                        pd.Index]:

    # Création de l'array des pct returns
    pct_returns_array = pct_returns_df.to_numpy(dtype=np.float32)

    # Création du DataFrame des prix avec des NaN
    prices_df = pd.DataFrame(equity_curves_calculs(pct_returns_df.values),
                             index=pct_returns_df.index,
                             columns=pct_returns_df.columns,
                             dtype=np.float32)

    prices_array = prices_df.to_numpy(dtype=np.float32)
    
    log_returns_array = log_returns_np(prices_array)
    hv_array = mt.hv_composite(pct_returns_array)

    asset_names = list(pct_returns_df.columns)
    dates = pct_returns_df.index

    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(pct_returns_array, hv_array)
    
    return prices_array, volatility_adjusted_pct_returns, log_returns_array, asset_names, dates

def calculate_ratios_returns(returns_df: pd.DataFrame, asset_names: list) -> pd.DataFrame:

    pair_returns_list = []
    
    for asset1, asset2 in combinations(asset_names, 2):
        pair_name = f"{asset1}-{asset2}"
        if asset1 in returns_df.columns and asset2 in returns_df.columns:
            pair_returns = returns_df[asset1] - returns_df[asset2]
            pair_returns_list.append(pair_returns.rename(f"{asset1}-{asset2}"))
    
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

def adjust_returns_for_inversion(returns_df: pd.DataFrame, columns_list: list) -> pd.DataFrame:

    for column in columns_list:

        returns = returns_df[column]

        inverted_returns = returns * -1
        
        inverted_returns_df = inverted_returns.to_frame(name=column)

        returns_df[column] = inverted_returns_df
    
    return returns_df