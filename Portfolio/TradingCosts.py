import pandas as pd
import numpy as np
import Metrics as mt
import bottleneck as bn

def calculate_cost_limit(raw_rolling_sharpe_df: pd.DataFrame, net_rolling_sharpe_df: pd.DataFrame, asset_names: list, limit_treshold=0.05, ma_window=250, day_treshold = 60) -> pd.DataFrame:
    """
    Calcule l'impact des coûts de transaction sur le ratio de Sharpe pour chaque actif, en utilisant la moyenne mobile.

    Parameters:

    - raw_rolling_sharpe_df : pd.DataFrame : DataFrame contenant les ratios de Sharpe bruts calculés sur une fenêtre de temps donnée.
    - net_rolling_sharpe_df : pd.DataFrame : DataFrame contenant les ratios de Sharpe nets calculés sur une fenêtre de temps donnée.
    - asset_names : list : Liste des noms des actifs à analyser.
    - limit_treshold : float : pourcentage de différence maximal accepté pour la limite de coût
    - ma_window : int : fenêtre de temps pour le calcul de la moyenne mobile
    
    Returns:

    - cost_validation_df : pd.DataFrame : DataFrame indiquant l'impact des coûts de transaction sur le ratio de Sharpe pour chaque actif.
    """
    # Initialisation du DataFrame d'impact
    cost_validation_df = pd.DataFrame(0, 
                                        index=raw_rolling_sharpe_df.index, 
                                        columns=raw_rolling_sharpe_df.columns, 
                                        dtype=np.float32
                                        )

    for asset in asset_names:
        # Filtrer les colonnes qui contiennent le nom de l'actif
        raw_sharpe_columns = [col for col in raw_rolling_sharpe_df.columns if asset in col]
        net_sharpe_columns = [col for col in net_rolling_sharpe_df.columns if asset in col]
        
        raw_sharpe = raw_rolling_sharpe_df[raw_sharpe_columns].values
        net_sharpe = net_rolling_sharpe_df[net_sharpe_columns].values
        
        # Calcul de la différence absolue
        sharpe_diff = (raw_sharpe + 100) - (net_sharpe + 100)
        
        # Calcul de la moyenne mobile de la différence de Sharpe
        ma_sharpe_diff = bn.move_mean(sharpe_diff, window=ma_window, min_count=1, axis=0)
        
        # Conditions pour déterminer si les coûts de transaction sont trop élevés
        positive_invalid_costs = (raw_sharpe > 0) & (ma_sharpe_diff > (raw_sharpe * limit_treshold))
        negative_invalid_costs = (raw_sharpe < 0) & (ma_sharpe_diff > ((raw_sharpe * limit_treshold)*-1))

        # Combinaison des deux conditions
        invalid_costs = positive_invalid_costs | negative_invalid_costs

        # Comptage des jours consécutifs où invalid_costs est vrai
        consecutive_days = np.zeros_like(invalid_costs, dtype=int)
        for i in range(1, len(invalid_costs)):
            consecutive_days[i] = np.where(invalid_costs[i], consecutive_days[i-1] + 1, 0)
        
        # Validation des coûts si invalid_costs est vrai pendant X jours consécutifs
        cost_validation_df[raw_sharpe_columns] = np.where(consecutive_days >= day_treshold, 0, 1)
    
    return cost_validation_df


def adjust_returns_by_impact(net_adjusted_returns_df: pd.DataFrame, cost_validation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajuste le DataFrame des rendements nets en fonction de l'impact des coûts de transaction.

    Parameters:
    - net_adjusted_returns_df : pd.DataFrame : DataFrame contenant les rendements nets ajustés.
    - cost_validation_df : pd.DataFrame : DataFrame indiquant l'impact des coûts de transaction sur le ratio de Sharpe pour chaque actif.

    Returns:
    - adjusted_returns_df : pd.DataFrame : DataFrame des rendements nets ajustés par l'impact des coûts de transaction.
    """
    # Ajustement des rendements nets en utilisant l'impact des coûts de transaction
    adjusted_returns_df = net_adjusted_returns_df * cost_validation_df

    return adjusted_returns_df

def calculate_cost_adjusted_returns(raw_adjusted_returns_df: pd.DataFrame, 
                                    net_adjusted_returns_df: pd.DataFrame, 
                                    asset_names: list, 
                                    window_size: int = 250) -> pd.DataFrame:
    """
    Calcule les rendements ajustés après prise en compte de l'impact du coût.
    
    Args:
    - raw_adjusted_returns_df: DataFrame des rendements bruts ajustés.
    - net_adjusted_returns_df: DataFrame des rendements nets ajustés.
    - asset_names: Liste des noms des actifs.
    - window_size: Taille de la fenêtre pour calculer les Sharpe ratios roulants (par défaut 250).

    Retourne:
    - cost_adjusted_returns_df: DataFrame des rendements ajustés après prise en compte des coûts.
    """
    # Calcul des Sharpe ratios roulants pour les rendements bruts et nets
    raw_rolling_sharpe_df = pd.DataFrame(mt.rolling_sharpe_ratios(raw_adjusted_returns_df, window_size, window_size),
                                         index=raw_adjusted_returns_df.index,
                                         columns=raw_adjusted_returns_df.columns)
    
    net_rolling_sharpe_df = pd.DataFrame(mt.rolling_sharpe_ratios(net_adjusted_returns_df, window_size, window_size),
                                         index=net_adjusted_returns_df.index,
                                         columns=net_adjusted_returns_df.columns)
    
    # Calcul de la limite des coûts en fonction des Sharpe ratios
    cost_validation_df = calculate_cost_limit(raw_rolling_sharpe_df, net_rolling_sharpe_df, asset_names)
    
    # Ajustement des rendements nets en fonction de l'impact des coûts
    cost_adjusted_returns_df = adjust_returns_by_impact(net_adjusted_returns_df, cost_validation_df)
    
    return cost_adjusted_returns_df
