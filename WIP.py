'''
import numbagg as nb

def rolling_mean_(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return nb.move_mean(array, window=length, min_count=min_length, axis=0)

def rolling_sum_(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return nb.move_sum(array, window=length, min_count=min_length, axis=0)

def rolling_volatility_(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return nb.move_std(array, window=length, min_count=min_length, axis=0)
'''

#data_prices_df_merged = MergeData.raccommoder_prices_futures_etf(data_prices_df, data_prices_df_yahoo, paires_futures_etf)

#data_prices_df_merged.to_csv(file_path_main_data)

#test = CleanData.adjust_prices_with_risk_free_rate(etf_data, bill_data)


'''
import pandas as pd
import numpy as np
import glob

# 1. Charger tous les fichiers CSV dans un seul DataFrame
def load_contracts_data(folder_path: str) -> pd.DataFrame:
    """
    Load and combine the 'Date', 'Close', 'Volume', and 'OpenInt' columns from all CSV files in a folder
    into a single DataFrame, with the contract name extracted from the filename.
    
    Parameters:
    ----------
    folder_path : str
        Path to the folder containing CSV files.

    Returns:
    -------
    pd.DataFrame
        Combined DataFrame with data from all contracts, indexed by 'Date'.
    """
    files = glob.glob(f"{folder_path}/*.csv")
    data_lst = []

    for file in files:
        # Extract contract name from filename
        contract = os.path.basename(file).replace(".csv", "")

        # Load only the required columns from the CSV file
        df = pd.read_csv(file, usecols=["Date", "Close", "Volume", "OpenInt"], parse_dates=["Date"], dayfirst=False)
        
        # Add contract name as a new column
        df["Contract"] = contract
        data_lst.append(df)

    # Concatenate all data into a single DataFrame and set 'Date' as the index
    contracts_df = pd.concat(data_lst, ignore_index=True).set_index("Date")

    return contracts_df


# 2. Calculer la MA10 du volume pour chaque contrat
def calculate_moving_average_volume(contracts_df, lookback=5):
    """
    Calcule la moyenne mobile du volume pour chaque contrat.
    
    Paramètres:
    - contracts_df: DataFrame contenant les données de tous les contrats

    Retour:
    - contracts_df avec la colonne ajoutée 'Mean_Volume'
    """
    contracts_df["Mean_OI"] = contracts_df.groupby("Contract")["OpenInt"].transform(lambda x: x.rolling(lookback, min_periods=1).mean())
    contracts_df["Mean_Volume"] = contracts_df.groupby("Contract")["Volume"].transform(lambda x: x.rolling(lookback, min_periods=1).mean())

    return contracts_df


def create_continuous_price_series(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a continuous series of prices based on the contract with the highest mean volume each day.
    
    Parameters:
    ----------
    prices_df : pd.DataFrame
        DataFrame with columns:
            - 'Date' (datetime): The date of each observation.
            - 'Close' (float): Closing price of each contract.
            - 'Mean_Volume' (float): Moving average of contract volume.
            - 'Contract' (str): Contract identifier.

    Returns:
    -------
    pd.DataFrame
        DataFrame with 'Date' as index, continuous 'Close' prices, and 'Contract_Change' column indicating changes.
    """
    # Sort by 'Date' and 'Mean_Volume' to select contracts with the highest average volume per day
    prices_df_sorted = prices_df.sort_values(['Date', 'Mean_OI', 'Mean_Volume'], ascending=[True, False, False])

    # Group by 'Date' to get the contract with the highest Mean_Volume each day
    highest_liquidity_df = prices_df_sorted.groupby('Date').first().reset_index()

    # Identify contract changes
    highest_liquidity_df['Contract_Change'] = highest_liquidity_df['Contract'] != highest_liquidity_df['Contract'].shift()

    return highest_liquidity_df[['Date', 'Close', 'Contract', 'Contract_Change']].set_index('Date')


def backadjust_price_series(unadjusted_df: pd.DataFrame, use_price_diff: bool = False) -> pd.DataFrame:
    """
    Applique un ajustement en arrière des prix de futures pour maintenir la continuité historique.
    Utilise soit un ajustement par différence de prix, soit un ajustement par ratio, en appliquant
    les ajustements en sens inverse du temps.

    Parameters:
    ----------
    unadjusted_df : pd.DataFrame
        DataFrame des prix non ajustés avec les jours de roll identifiés (index en datetime, Close, Contract_Change).
    use_price_diff : bool, optional
        Choisit le mode d'ajustement : True pour ajustement par différence de prix, False pour ajustement par ratio (par défaut False).

    Returns:
    -------
    pd.DataFrame
        DataFrame avec 'Date' comme index et les prix ajustés en continuité.
    """
    cumulative_adjustment = 0.0 if use_price_diff else 1.0

    adjusted_close_lst = unadjusted_df['Close'].copy()

    # Parcours du DataFrame de bas en haut pour appliquer l'ajustement en arrière
    for i in range(len(unadjusted_df) - 1, 0, -1):
        if unadjusted_df['Contract_Change'].iloc[i] == True:
            # Calcul du ratio ou de la différence entre le contrat actuel et le précédent
            next_close = unadjusted_df['Close'].iloc[i]
            previous_close = unadjusted_df['Close'].iloc[i - 1]
            
            if use_price_diff:
                # Calcul de l'ajustement en arrière par différence
                price_diff = next_close - previous_close
                cumulative_adjustment += price_diff
            else:
                # Calcul de l'ajustement en arrière par ratio
                price_ratio = next_close / previous_close
                cumulative_adjustment *= price_ratio

        # Appliquer l'ajustement cumulatif aux prix antérieurs
        adjusted_close_lst.iloc[i - 1] = (adjusted_close_lst.iloc[i - 1] + cumulative_adjustment 
                                          if use_price_diff 
                                          else adjusted_close_lst.iloc[i - 1] * cumulative_adjustment)

    # Mise à jour du DataFrame avec les prix ajustés
    unadjusted_df['Close'] = adjusted_close_lst

    # Renvoie uniquement la colonne des prix ajustés avec 'Date' comme index
    final_adjusted_df = unadjusted_df[['Close']]

    return final_adjusted_df


def identify_roll_dates(adjusted_df: pd.DataFrame, unadjusted_df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifie les jours de roll en calculant la variation en pourcentage entre les prix ajustés et non ajustés,
    et considère un jour de roll lorsque la variation dépasse 0.
    
    Parameters:
    ----------
    adjusted_df : pd.DataFrame
        DataFrame des prix ajustés (Date, Close).
    unadjusted_df : pd.DataFrame
        DataFrame des prix non ajustés (Date, Close).

    Returns:
    -------
    pd.DataFrame
        DataFrame original des prix non ajustés avec la colonne 'Roll_Day' ajoutée.
    """
    # Calculer la variation en pourcentage entre les prix ajustés et non ajustés
    unadjusted_df['Price_Diff'] = adjusted_df['Close'] - unadjusted_df['Close']

    unadjusted_df['Price_Diff_Change'] = unadjusted_df['Price_Diff'].pct_change().round(2)

    # Identifier les jours de roll (quand la variation en pourcentage dépasse le seuil)
    unadjusted_df['Roll_Day'] = (unadjusted_df['Price_Diff_Change'].abs() > 0).astype(int)
    
    # Supprimer la colonne temporaire 'Price_Diff'
    #unadjusted_df.drop(columns=['Price_Diff'], inplace=True)
    
    return unadjusted_df


def apply_adjustment(unadjusted_df: pd.DataFrame, use_price_diff: bool = False) -> pd.DataFrame:
    """
    Applique un ajustement en arrière des prix de futures pour maintenir la continuité historique.
    Utilise soit un ajustement par différence de prix, soit un ajustement par ratio.

    Parameters:
    ----------
    unadjusted_df : pd.DataFrame
        DataFrame des prix non ajustés avec les jours de roll identifiés (index en datetime, Close, Roll_Day).
    use_price_diff : bool, optional
        Choisit le mode d'ajustement : True pour ajustement par différence de prix, False pour ajustement par ratio (par défaut False).

    Returns:
    -------
    pd.DataFrame
        DataFrame avec 'Date' comme index et les prix ajustés en continuité.
    """
    cumulative_adjustment = 0.0 if use_price_diff else 1.0

    adjusted_close_lst = unadjusted_df['Close'].copy()

    # Parcours du DataFrame de bas en haut pour appliquer l'ajustement en arrière
    for i in range(len(unadjusted_df) - 1, 0, -1):
        if unadjusted_df['Roll_Day'].iloc[i] == 1:
            # Calcul du ratio ou de la différence entre le contrat actuel et le précédent
            next_close = unadjusted_df['Close'].iloc[i]
            previous_close = unadjusted_df['Close'].iloc[i - 1]
            
            if use_price_diff:
                # Calcul de l'ajustement en arrière par différence
                price_diff = next_close - previous_close
                cumulative_adjustment += price_diff
            else:
                # Calcul de l'ajustement en arrière par ratio
                price_ratio = next_close / previous_close
                cumulative_adjustment *= price_ratio

        # Appliquer l'ajustement cumulatif aux prix antérieurs
        adjusted_close_lst.iloc[i - 1] = (adjusted_close_lst.iloc[i - 1] + cumulative_adjustment 
                                          if use_price_diff 
                                          else adjusted_close_lst.iloc[i - 1] * cumulative_adjustment)

    # Mise à jour du DataFrame avec les prix ajustés
    unadjusted_df['Close'] = adjusted_close_lst

    # Renvoie uniquement la colonne des prix ajustés avec 'Date' comme index
    final_adjusted_df = unadjusted_df[['Close']]

    return final_adjusted_df

adjusted_front_df = pd.read_csv(
    "D:\\Python\\Data\\Excel_Data\\TradingView\\AdjustedFrontMonth\\VX.csv",
    usecols=['time', 'close'],
    parse_dates=['time']
).rename(columns={'time': 'Date', 'close': 'Close'}).set_index('Date')

unadjusted_front_df = pd.read_csv(
    "D:\\Python\\Data\\Excel_Data\\TradingView\\UnadjustedFrontMonth\\VX.csv",
    usecols=['time', 'close'],
    parse_dates=['time']
).rename(columns={'time': 'Date', 'close': 'Close'}).set_index('Date')

# Identification des jours de roll
roll_dates_df = identify_roll_dates(adjusted_front_df, unadjusted_front_df)

# Ajustement des prix
Final_adjusted_prices_df = apply_adjustment(roll_dates_df, use_price_diff=False)
'''

#relativized_sharpes_df = RollingSharpe.relative_sharpe_on_confidence_period(raw_adjusted_returns_df, sharpe_lookback = 5000, confidence_lookback=2500)
#optimized_returns_rltv = raw_adjusted_returns_df * relativized_sharpes_df.shift(1)

'''
from joblib import Parallel, delayed
import pandas as pd
import numpy as np
def extract_asset_groups(portfolio_dict):
    """
    Fonction récursive pour extraire toutes les listes d'actifs d'un dictionnaire imbriqué.
    
    Parameters:
    - portfolio_dict: Dictionnaire définissant les groupes et sous-groupes d'actifs.
    
    Returns:
    - asset_groups: Liste de toutes les listes d'actifs trouvées dans le dictionnaire.
    """
    asset_groups = []
    
    def recursive_extract(d):
        for key, value in d.items():
            if isinstance(value, dict):
                recursive_extract(value)  # Continuer à explorer si c'est un sous-dictionnaire
            elif isinstance(value, list):
                asset_groups.append(value)  # Ajouter la liste d'actifs trouvée
            else:
                raise ValueError("Structure inattendue dans le dictionnaire.")
    
    recursive_extract(portfolio_dict)
    
    return asset_groups


def compute_group_diversification_multiplier(group_returns, weights, window):
    """
    Calcule le multiplicateur de diversification pour un groupe d'actifs sur une base roulante.

    Parameters:
    - group_returns: DataFrame des rendements du groupe d'actifs.
    - weights: Array de poids pour les actifs du groupe.
    - window: taille de la fenêtre pour la corrélation roulante.

    Returns:
    - diversification_multiplier_series: Série des multiplicateurs de diversification pour chaque date.
    """
    # Calcul de la matrice de corrélation roulante
    rolling_corr = group_returns.rolling(window=window).corr(pairwise=True)

    # Calcul du multiplicateur de diversification
    num_assets = len(weights)
    diversification_multipliers = []

    for i in range(window - 1, len(group_returns)):
        # Extraire la sous-matrice de corrélation pour chaque fenêtre
        corr_matrix = rolling_corr.iloc[i * num_assets: (i + 1) * num_assets].values.reshape(num_assets, num_assets)
        
        # Calcul de la variance pondérée et du multiplicateur pour cette fenêtre
        weighted_variance = weights @ corr_matrix @ weights
        diversification_multiplier = 1.0 / np.sqrt(weighted_variance) if weighted_variance > 0 else 1.0
        diversification_multipliers.append(diversification_multiplier)

    # Convertir en série en alignant les index avec les dates de rolling_corr
    diversification_multiplier_series = pd.Series([np.nan] * (window - 1) + diversification_multipliers, 
                                                  index=group_returns.index, dtype=np.float32)

    return diversification_multiplier_series



def compute_diversification_for_group(group_assets, returns_df, window):
    """
    Calcule la série de multiplicateurs de diversification pour un groupe spécifique d'actifs.
    
    Parameters:
    - group_assets: Liste des actifs dans le groupe.
    - returns_df: DataFrame des rendements pour tous les actifs.
    - window: Taille de la fenêtre pour la corrélation roulante.
    
    Returns:
    - Series des multiplicateurs de diversification avec index aligné sur returns_df.
    - Liste d'actifs du groupe pour assignation directe.
    """
    group_returns = returns_df[group_assets]
    weights = np.full(len(group_assets), 1.0 / len(group_assets), dtype=np.float32)

    diversification_multiplier_series = compute_group_diversification_multiplier(
        group_returns, weights, window
    )
    
    return diversification_multiplier_series, group_assets

def diversification_multiplier_by_group(returns_df, portfolio_dict, window):
    """
    Calcule le multiplicateur de diversification pour chaque actif dans un DataFrame de rendements,
    en utilisant les listes d'actifs définies dans le dictionnaire, sur une base roulante, avec parallélisation.
    
    Parameters:
    - returns_df: DataFrame de rendements, chaque colonne correspondant à un actif.
    - portfolio_dict: Dictionnaire définissant les groupes et sous-groupes d'actifs.
    - window: Taille de la fenêtre pour la corrélation roulante.
    
    Returns:
    - diversification_multiplier_df: DataFrame des multiplicateurs de diversification.
    """
    # Extraire toutes les listes d'actifs depuis le dictionnaire
    asset_groups = extract_asset_groups(portfolio_dict)
    
    # Filtrer les groupes pour ne garder que ceux avec plus d'un actif dans returns_df
    valid_groups = [group for group in asset_groups if len([asset for asset in group if asset in returns_df.columns]) > 1]

    # Initialiser le DataFrame pour les multiplicateurs de diversification
    diversification_multiplier_df = pd.DataFrame(1.0, index=returns_df.index, columns=returns_df.columns, dtype=np.float32)

    # Calcul parallèle pour chaque groupe valide
    results = Parallel(n_jobs=-1)(delayed(compute_diversification_for_group)(
        [asset for asset in group if asset in returns_df.columns], 
        returns_df, 
        window
    ) for group in valid_groups)

    # Combiner les résultats dans le DataFrame final
    for diversification_multiplier_series, group_assets in results:
        for asset in group_assets:
            diversification_multiplier_df.loc[diversification_multiplier_series.index, asset] = diversification_multiplier_series

    # Remplacer tous les NaN restants par 1.0
    diversification_multiplier_df.fillna(1.0, inplace=True)

    diversification_multiplier_df = diversification_multiplier_df.rolling(window=250, min_periods=1).mean()
    
    return diversification_multiplier_df

#test_diversification_multipliers = diversification_multiplier_by_group(test_asset_returns,portfolio_base_structure, 2500)
'''


'''
# FONCTIONNE, PLUS QU'A METTRE EN PLACE AJUSTEMENT POUR TAILLE DE CONTRAT ET RENVOI PAR LISTE ET ON EST BONS
def calculate_shares_to_trade_from_adjusted_return(portfolio_size, asset_price, adjusted_return):
    """
    Calcule le nombre d'actions à acheter ou vendre en fonction du rendement ajusté de l'asset.

    Args:
        portfolio_size (float): La taille totale du portefeuille en $.
        asset_price (float): Le prix actuel de l'asset en $.
        adjusted_return (float): Le rendement en % ajusté (incluant l'allocation d'actif et la taille du signal).

    Returns:
        float: Nombre d'actions à acheter (positif) ou vendre (négatif).
    """

    # Calcul du montant total à investir en fonction du rendement ajusté
    amount_to_invest = portfolio_size * (adjusted_return * 100)

    # Calcul du nombre d'actions à acheter ou vendre
    shares_to_trade = amount_to_invest / asset_price

    return round(shares_to_trade)

portfolio_size = 371369
asset_price = 6307
adjusted_return = -0.000928 # Rendement ajusté en %

# Calcul du nombre d'actions à acheter ou vendre
shares_to_trade = calculate_shares_to_trade_from_adjusted_return(portfolio_size, asset_price, adjusted_return)
print(f"Position optimale : {shares_to_trade:.2f}")
'''