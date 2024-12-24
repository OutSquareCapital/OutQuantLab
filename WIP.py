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


paires_futures_etf = [
("6A", "AD"),
("6B", "BP"),
("6C", "CD"),
("YM", "1YM"),
("RTY", "TF"),
("RTY", "SMC"),
("6E", "URO"),
("ZS", "S"),
("ZC", "C"),
("ZW", "W"),
("ES", "SP"),
("ZB", "US"),
("ZF", "FV"),
]

portfolio_futures = {
    'Equities': {
        'Large Caps': ['ES', 'YM', 'NQ'],
        'Small Caps': ['RTY'],
        'Volatility': ['VX'],
    },
    'Bonds': {
        'US':['ZF'],
    },
    'Currencies': {
        'Precious Metals': ['GC', 'SI'],
        'FX': ['6A', '6E', '6B', '6C'],
        'Crypto': ['BTC'],
    },
    'Commodities': {
    'Agricultural': ['ZC', 'ZW', 'ZS'],
    'Energy': ['CL', 'NG'],
    'Base Metals': ['HG'],
    }
}
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
'''
from scipy.stats import norm, rankdata
def normalize_returns_distribution_rolling(
    pct_returns_df: pd.DataFrame, 
    window_size: int
    ) -> pd.DataFrame:
    
    normalized_returns = pd.DataFrame(
        index=pct_returns_df.index, 
        columns=pct_returns_df.columns, 
        dtype=np.float32)

    for end in range(window_size - 1, len(pct_returns_df)):
        window_df = pct_returns_df.iloc[end - window_size + 1 : end + 1]
        
        window_df_shifted = window_df.shift(1)
        window_df_shifted.fillna(0, inplace=True)
        returns = window_df_shifted.values
        
        mean_returns = np.mean(returns, axis=0)
        std_returns = np.std(returns, axis=0)
        
        ranks = np.apply_along_axis(lambda x: rankdata(x) / (len(x) + 1), axis=0, arr=returns)
        
        normalized_returns_window = norm.ppf(ranks)
        
        normalized_returns_window = normalized_returns_window * std_returns + mean_returns
        
        normalized_returns.iloc[end] = normalized_returns_window[-1]

    return normalized_returns
'''
'''
from joblib import Parallel, delayed
import pandas as pd
import numpy as np
def extract_asset_groups(portfolio_dict):

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

    rolling_corr = group_returns.rolling(window=window).corr(pairwise=True)

    num_assets = len(weights)
    diversification_multipliers = []

    for i in range(window - 1, len(group_returns)):
        corr_matrix = rolling_corr.iloc[i * num_assets: (i + 1) * num_assets].values.reshape(num_assets, num_assets)
        
        weighted_variance = weights @ corr_matrix @ weights
        diversification_multiplier = 1.0 / np.sqrt(weighted_variance) if weighted_variance > 0 else 1.0
        diversification_multipliers.append(diversification_multiplier)

    diversification_multiplier_series = pd.Series(
        [np.nan] * (window - 1) + diversification_multipliers, 
        index=group_returns.index, 
        dtype=np.float32
        )

    return diversification_multiplier_series

def compute_diversification_for_group(group_assets, returns_df, window):

    group_returns = returns_df[group_assets]
    weights = np.full(len(group_assets), 1.0 / len(group_assets), dtype=np.float32)

    diversification_multiplier_series = compute_group_diversification_multiplier(
        group_returns, weights, window
    )
    
    return diversification_multiplier_series, group_assets

def diversification_multiplier_by_group(returns_df, portfolio_dict, window):

    asset_groups = extract_asset_groups(portfolio_dict)
    valid_groups = [group for group in asset_groups if len([asset for asset in group if asset in returns_df.columns]) > 1]

    diversification_multiplier_df = pd.DataFrame(1.0, index=returns_df.index, columns=returns_df.columns, dtype=np.float32)

    results = Parallel(n_jobs=-1)(delayed(compute_diversification_for_group)(
        [asset for asset in group if asset in returns_df.columns], 
        returns_df, 
        window
    ) for group in valid_groups)

    for diversification_multiplier_series, group_assets in results:
        for asset in group_assets:
            diversification_multiplier_df.loc[diversification_multiplier_series.index, asset] = diversification_multiplier_series

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

'''

def snapshot_at_intervals(prices_array: np.ndarray, snapshot_interval: int) -> np.ndarray:

    snapshot_indices = np.arange(0, prices_array.shape[0], snapshot_interval)

    snapshots = prices_array[snapshot_indices]

    repeated_snapshots = np.repeat(snapshots, snapshot_interval, axis=0)

    repeated_snapshots = repeated_snapshots[:prices_array.shape[0]]

    return repeated_snapshots

def seasonal_breakout_returns(prices_array: np.ndarray, LengthMean: int, LengthSnapshot: int, amplitude: int)-> np.ndarray:
    
    # Capture les snapshots à des intervalles réguliers
    repeated_snapshots_array = ft.snapshot_at_intervals(prices_array, LengthSnapshot)

    # Calcul des rendements par rapport aux snapshots
    returns = (prices_array / repeated_snapshots_array) - 1

    abs_returns_array = abs(returns)

    avg_move = SeasonalBreakout.calculate_avg_move_nan(abs_returns_array, LengthSnapshot, LengthMean)

    amplitude_float = np.float32(amplitude)
    amplitude_adjustement = np.float32(10)

    adjusted_amplitude = amplitude_float / amplitude_adjustement

    # Définition des bornes basées sur la moyenne glissante
    upper_bound = avg_move * adjusted_amplitude
    lower_bound = -avg_move * adjusted_amplitude

    signals = np.where(np.isnan(returns) | np.isnan(upper_bound) | np.isnan(lower_bound), np.nan,  # Si l'un des trois est NaN, signal est NaN
                    np.where(returns > upper_bound, 1,  # Si returns > upper_bound, signal est 1 (achat)
                                np.where(returns < lower_bound, -1, 0)))  # Si returns < lower_bound, signal est -1 (vente), sinon 0
    
    # Forcer le tableau signals en float32
    signals = signals.astype(np.float32)

    return signals*-1

@njit
def calculate_avg_move_nan(abs_returns_np: np.ndarray, LengthSnapshot:int, LengthMean:int):
    """
    Calculer la moyenne des mouvements absolus des rendements en excluant les NaN
    sur une fenêtre de temps basée sur LengthPeriod et LengthMean.

    Args:
        abs_returns_np (np.ndarray): Un tableau 2D de rendements absolus (chaque colonne représente un actif).
        LengthPeriod (int): La période entre chaque snapshot (prise de vue) dans l'historique.
        LengthMean (int): Le nombre de snapshots à inclure dans le calcul de la moyenne.

    Returns:
        np.ndarray: Un tableau 2D où chaque cellule contient la moyenne des rendements sur la fenêtre, ou NaN si aucune donnée n'est disponible.
    """
    
    # Obtenir les dimensions du tableau de rendements : num_days est le nombre de lignes (jours), num_assets le nombre d'actifs (colonnes)
    num_days, num_assets = abs_returns_np.shape

    # Créer un tableau vide pour stocker les moyennes calculées pour chaque jour et chaque actif
    avg_move = np.empty((num_days, num_assets), dtype=np.float32)

    # Boucle sur chaque jour i (chaque ligne)
    for i in range(num_days):
        # Générer les indices des snapshots à utiliser pour le calcul de la moyenne
        # Commence à i, puis recule de LengthPeriod à chaque étape, et ne conserve que les LengthMean premiers indices
        snapshot_indices = np.arange(i, -1, -LengthSnapshot)[:LengthMean]

        # Initialiser les variables pour stocker la somme des rendements et le nombre de valeurs valides (non-NaN) pour chaque actif
        total_sum = np.zeros(num_assets, dtype=np.float32)  # Tableau pour accumuler les sommes de rendements par actif
        valid_count = np.zeros(num_assets, dtype=np.float32)  # Compteur du nombre de valeurs valides (non-NaN) par actif

        # Boucle sur les indices des snapshots sélectionnés
        for idx in snapshot_indices:
            # Extraire les rendements pour chaque actif à l'index donné (snapshot)
            values = abs_returns_np[idx]

            # Pour chaque actif, vérifier s'il s'agit d'une valeur valide (non-NaN)
            for asset_idx in range(num_assets):
                if not np.isnan(values[asset_idx]):  # Si la valeur n'est pas NaN, l'inclure dans le calcul
                    total_sum[asset_idx] += values[asset_idx]  # Ajouter la valeur à la somme courante pour cet actif
                    valid_count[asset_idx] += 1  # Incrémenter le compteur de valeurs valides pour cet actif

        # Calculer la moyenne des rendements pour chaque actif, seulement si des valeurs valides ont été trouvées
        for asset_idx in range(num_assets):
            if valid_count[asset_idx] > 0:
                # Diviser la somme totale par le nombre de valeurs valides pour obtenir la moyenne
                avg_move[i, asset_idx] = total_sum[asset_idx] / valid_count[asset_idx]
            else:
                # Si aucune valeur valide n'a été trouvée, renvoyer NaN pour cet actif
                avg_move[i, asset_idx] = np.nan

    # Retourner le tableau des moyennes calculées (ou NaN si aucune donnée valide)
    return avg_move

    @staticmethod
    def seasonal_breakout_returns_trend(prices_array: np.ndarray, LengthMean: int, LengthSnapshot: int, amplitude: int, LenST: int, LenLT: int) -> np.ndarray:

        seasonal_breakout_signal = SeasonalBreakout.seasonal_breakout_returns(prices_array, LengthMean, LengthSnapshot, amplitude)

        trend_signal = Trend.mean_price_ratio(prices_array, LenST, LenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, seasonal_breakout_signal)
'''

'''
def generate_group_mask(seasonal_array: np.ndarray, GroupBy: int, GroupSelected: int):
    # Utiliser les positions des colonnes saisonnières directement
    # Position 0 : 'DayOfWeek', Position 1 : 'WeekOfMonth', Position 2 : 'QuarterOfYear'
    return seasonal_array[:, GroupBy - 1] == GroupSelected

@staticmethod
def generate_seasonal_trend_signal(
    returns_array: np.ndarray,
    group_mask_array: np.ndarray, 
    LenST: int, 
    LenLT: int
) -> np.ndarray:

    # Extraction des retours sélectionnés en fonction du masque de groupe
    selected_returns_array = returns_array[group_mask_array]
    
    mean_returns = mt.rolling_mean(selected_returns_array, length=LenST, min_length=1)
    mean_roc_raw = mt.rolling_sum(mean_returns, length=LenLT, min_length=4)
    seasonal_trend_signal = sn.sign_normalization(mean_roc_raw)

    return ft.shift_array(seasonal_trend_signal)


@staticmethod
def process_trend_signal(
    seasonal_trend_signal: np.ndarray, 
    group_mask_array: np.ndarray,
    shape: tuple
) -> np.ndarray:
    
    processed_seasonal_trend_signal = np.zeros(shape, dtype=np.float32)
    processed_seasonal_trend_signal[group_mask_array] = seasonal_trend_signal

    return processed_seasonal_trend_signal

@staticmethod
def generate_conditioned_seasonal_trend_signal(
    returns_array: np.ndarray,
    group_mask_array: np.ndarray,
    LenST: int, 
    LenLT: int,
    TrendLenST: int, 
    TrendLenLT: int
) -> np.ndarray:

    seasonal_trend_signal = Seasonality.generate_seasonal_trend_signal(returns_array, group_mask_array, LenST, LenLT)

    # Calcul de la tendance générale sur l'ensemble des données
    general_trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

    # Décalage en arrière de la tendance générale pour éviter le lookahead journalier
    general_trend_signal = ft.shift_array(general_trend_signal)

    return sn.calculate_indicator_on_trend_signal(general_trend_signal[group_mask_array], seasonal_trend_signal)

@staticmethod
def seasonal_trend( returns_array: np.ndarray,
                    seasonal_array: np.ndarray,
                    GroupBy: int, 
                    GroupSelected: int, 
                    LenST: int, 
                    LenLT: int) -> np.ndarray:

    group_mask_array = Seasonality.generate_group_mask(seasonal_array, GroupBy, GroupSelected)

    seasonal_trend_signal = Seasonality.generate_seasonal_trend_signal(returns_array, group_mask_array, LenST, LenLT)

    processed_seasonal_trend_signal = Seasonality.process_trend_signal(seasonal_trend_signal, 
                                                                        group_mask_array, 
                                                                        returns_array.shape)

    return np.roll(processed_seasonal_trend_signal, -1, axis=0)


@staticmethod
def overall_seasonal_trend(returns_array: np.ndarray,
                            seasonal_array: np.ndarray,
                            GroupBy: int, 
                            GroupSelected: int, 
                            LenST: int, 
                            LenLT: int,
                            TrendLenST: int, 
                            TrendLenLT: int        
                        ) -> np.ndarray:

    group_mask_array = Seasonality.generate_group_mask(seasonal_array, GroupBy, GroupSelected)
    
    seasonal_trend_conditioned_signal = Seasonality.generate_conditioned_seasonal_trend_signal(returns_array, 
                                                                                                group_mask_array, 
                                                                                                LenST, 
                                                                                                LenLT, 
                                                                                                TrendLenST, 
                                                                                                TrendLenLT)

    processed_seasonal_trend_conditioned_signal = Seasonality.process_trend_signal(seasonal_trend_conditioned_signal, 
                                                                                    group_mask_array, 
                                                                                    returns_array.shape)

    return np.roll(processed_seasonal_trend_conditioned_signal, -1, axis=0)
'''