import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from collections import defaultdict
from scipy.stats import skew
import Config
import Dashboard.Common as cmon
from Process_Data import equity_curves_calculs

def overall_sharpe_ratios_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    sharpe_ratios = daily_returns.mean() / daily_returns.std() * Config.ANNUALIZATION_FACTOR

    sharpe_ratios_df = pd.DataFrame(sharpe_ratios, columns=['Sharpe Ratio'], dtype=np.float32)

    return sharpe_ratios_df.round(2)

def overall_sortino_ratios_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    mean_returns = daily_returns.mean()
    
    downside_deviation = daily_returns[daily_returns < 0].std()
    
    sortino_ratios = mean_returns / downside_deviation * Config.ANNUALIZATION_FACTOR

    sortino_ratios_df = pd.DataFrame(sortino_ratios, columns=['Sortino Ratio'], dtype=np.float32)

    return sortino_ratios_df.round(2)

def calculate_final_equity_values(daily_returns: pd.DataFrame, initial_equity: int = 100000) -> pd.DataFrame:

    final_equities = []
    for start_date in daily_returns.index:
        # Calculer les courbes d'équité en utilisant cumprod depuis le start_date
        equity_curve = (1 + daily_returns.loc[start_date:]).cumprod() * initial_equity
        final_values = equity_curve.iloc[-1]
        final_equities.append(final_values)

    final_equities_df = pd.DataFrame(final_equities, 
                                        index=daily_returns.index, 
                                        columns=daily_returns.columns, 
                                        dtype=np.float32)

    return final_equities_df

def drawdowns_calculs(returns_df: pd.DataFrame) -> pd.DataFrame:

    equity_curves = equity_curves_calculs(returns_df)
    
    # Calculate drawdowns for each equity curve directly
    drawdowns = (equity_curves - equity_curves.cummax()) / equity_curves.cummax() * Config.PERCENTAGE_FACTOR
    drawdowns = drawdowns.round(2)

    return drawdowns

def annual_returns_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    # Grouper les rendements par année
    grouped = daily_returns.groupby(daily_returns.index.year)

    # Calculer les rendements cumulés pour chaque groupe (année)
    cumulative_returns = grouped.apply(lambda x: (x + 1).prod() - 1)

    # Conversion en DataFrame
    cumulative_returns_df = pd.DataFrame(cumulative_returns, dtype=np.float32)

    cumulative_returns_df = cumulative_returns_df.round(4) * Config.PERCENTAGE_FACTOR

    return cumulative_returns_df

def average_correlation_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    correlation_matrix = daily_returns.corr()
    average_correlations = correlation_matrix.mean()
    average_correlations_df = pd.DataFrame(average_correlations, 
                                            columns=['Average Correlation'], 
                                            dtype=np.float32)
    average_correlations_df = average_correlations_df.round(2)

    return average_correlations_df

def analyze_param_sensitivity(daily_returns: pd.DataFrame, params: list):

    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = overall_sharpe_ratios_calculs(daily_returns)

    param_values_list = []
    sharpe_ratios = []

    # Extraire les paramètres et les ratios de Sharpe
    for index, row in sharpe_ratios_df.iterrows():
        param_values = cmon.extract_all_params_from_name(index, params)
        if all(param_values):  # Vérifie si toutes les valeurs de paramètres sont présentes
            param_values_list.append(param_values)
            sharpe_ratios.append(row['Sharpe Ratio'])

    # Création d'un DataFrame pour les paramètres et les Sharpe Ratios
    param_values_df = pd.DataFrame(param_values_list, columns=params, dtype=np.float32)
    param_values_df['Sharpe Ratio'] = sharpe_ratios

    # Supprimer les lignes avec des NaN dans Sharpe Ratio
    param_values_df = param_values_df.dropna(subset=['Sharpe Ratio'])

    # Standardiser les paramètres pour que les échelles soient comparables
    scaler = StandardScaler()
    param_values_scaled = scaler.fit_transform(param_values_df[params])

    # Ajouter une constante pour l'ordonnée à l'origine
    X = sm.add_constant(param_values_scaled)
    y = param_values_df['Sharpe Ratio']

    # Effectuer la régression linéaire multiple
    model = sm.OLS(y, X).fit()

    # Résultats de la régression
    #print("\nRésumé de la régression OLS :")
    #print(model.summary())

    # Associer les noms de params au modèle
    param_coeffs = dict(zip(params, model.params[1:]))

    # Convertir en série pour manipulation facile
    coefficients = pd.Series(param_coeffs)

    # Trier les coefficients par valeur absolue pour voir l'importance relative
    sorted_coefficients = coefficients.abs().sort_values(ascending=False)

    #print("\nImportance des paramètres (en valeur absolue des coefficients de régression) :")
    #print(sorted_coefficients)

    return sorted_coefficients

def calculate_sharpe_correlation_ratio(daily_returns: pd.DataFrame) -> pd.DataFrame:

    # Calcul des Sharpe Ratios et des Average Correlations
    sharpe_ratios_df = overall_sharpe_ratios_calculs(daily_returns)
    average_correlations_df = average_correlation_calculs(daily_returns)

    # Calculer les rangs des Sharpe Ratios et des Correlations indépendamment
    sharpe_ratios_df['Sharpe Rank'] = sharpe_ratios_df['Sharpe Ratio'].rank(method='min')
    average_correlations_df['Correlation Rank'] = average_correlations_df['Average Correlation'].rank(method='min')

    # Fusionner les deux DataFrames avec pd.concat en s'assurant que les index sont alignés
    combined_df = pd.concat([sharpe_ratios_df, average_correlations_df], axis=1)

    # Calculer la nouvelle métrique : Sharpe Rank / Correlation Rank
    combined_df['Sharpe/AvgCorrelation'] = combined_df['Sharpe Rank'] / combined_df['Correlation Rank']

    return combined_df

def calculate_sharpe_means_from_combination(daily_returns, params):
    """
    Calcule les moyennes des Sharpe ratios pour chaque combinaison de trois paramètres.

    Args:
    daily_returns (pd.DataFrame): DataFrame contenant les retours journaliers des stratégies.
    params (list): Liste des paramètres à extraire des noms des stratégies.

    Returns:
    tuple: Contient quatre np.arrays : x_vals (param1), y_vals (param2), z_vals (param3), et sharpe_means (moyenne des Sharpe ratios).
    """
    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = overall_sharpe_ratios_calculs(daily_returns)

    # Initialiser un dictionnaire pour stocker les Sharpe ratios par combinaison de paramètres
    sharpe_dict = defaultdict(list)

    # Extraire les paramètres et les ratios de Sharpe à partir de l'index
    for index, row in sharpe_ratios_df.iterrows():
        param_values = cmon.extract_all_params_from_name(index, params)

        # Si on trouve toutes les valeurs de paramètres, on les utilise pour la clé du dictionnaire
        if all(param_values):  # Vérifie si toutes les valeurs de paramètres sont présentes
            # On utilise les trois premiers paramètres comme clé
            key = tuple(param_values[:3])
            sharpe_dict[key].append(row['Sharpe Ratio'])

    # Initialiser les listes pour les valeurs moyennes des Sharpe ratios
    x_vals = []
    y_vals = []
    z_vals = []
    sharpe_means = []

    # Calculer les moyennes des Sharpe ratios pour chaque combinaison (param1, param2, param3)
    for (p1, p2, p3), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(p3)
        sharpe_means.append(np.nanmean(sharpe_list))  # Moyenne des Sharpe ratios pour chaque combinaison

    # Convertir en np.array pour faciliter la manipulation
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)
    sharpe_means = np.array(sharpe_means)

    return x_vals, y_vals, z_vals, sharpe_means

def sharpe_ratios_yearly_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Sharpe ratios for each year.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.

    Returns:
        pd.DataFrame: DataFrame containing Sharpe ratios for each year.
    """
    # Grouper les retours par année
    grouped = daily_returns.groupby(daily_returns.index.year)

    # Calculer les ratios de Sharpe pour chaque groupe (année)
    sharpe_ratios = grouped.apply(lambda x: sharpe_ratios_yearly_calculs(x)['Sharpe Ratio'])

    # Conversion en DataFrame
    sharpe_ratios_df = pd.DataFrame(sharpe_ratios, dtype=np.float32)

    return sharpe_ratios_df

def overall_monthly_skew_calculs(returns_df: pd.DataFrame) -> pd.Series:
    """
    Agrège les retours quotidiens en rendements mensuels moyens et calcule le skew de cette série mensuelle 
    pour chaque actif.

    Parameters:
    - returns_df (pd.DataFrame): DataFrame des retours quotidiens avec un index datetime.

    Returns:
    - pd.Series: Série contenant le skew mensuel global pour chaque actif.
    """
    # Agréger par mois pour obtenir les rendements mensuels moyens pour chaque actif
    monthly_returns_df = returns_df.resample('ME').mean()
    
    # Calculer le skew sur les rendements mensuels pour chaque actif
    skew_series = monthly_returns_df.apply(lambda x: skew(x, nan_policy='omit')).astype(np.float32).round(2)
    
    return skew_series

def calculate_and_group_information_ratio(signals_df: pd.DataFrame, returns_df: pd.DataFrame, by_param=False, by_method=False, by_class=False, by_asset=False) -> pd.DataFrame:
    """
    Calculate the Information Coefficient (IC) between trading signals and future returns,
    and calculate average IC values based on specified grouping options.

    Args:
        signals_df (pd.DataFrame): DataFrame containing the trading signals.
        returns_df (pd.DataFrame): DataFrame containing the returns of the underlying assets.
        by_param (bool): Whether to group by parameter.
        by_method (bool): Whether to group by method.
        by_class (bool): Whether to group by class.
        by_asset (bool): Whether to group by asset.

    Returns:
        pd.DataFrame: DataFrame containing the average IC values.
    """
    # Calculate IC values
    ic_dict = {}
    future_returns_df = returns_df.shift(-1)

    for col in signals_df.columns:
        asset_name = col.split('_')[0]
        if asset_name in returns_df.columns:
            ic_value = signals_df[col].corr(future_returns_df[asset_name])
            ic_dict[col] = ic_value

    ic_df = pd.DataFrame(ic_dict, index=['IC'], dtype=np.float32)

    # Calculate averages based on specified grouping options
    if by_class and by_method:
        raise ValueError("Calculating averages by both 'class' and 'method' is not supported as methods belong to classes.")

    grouping_keys = []
    if by_asset:
        grouping_keys.append(0)  # Asset is in position 0
    if by_class:
        grouping_keys.append(1)  # Class is in position 1
    if by_method:
        grouping_keys.append(2)  # Method is in position 2
    if by_param:
        grouping_keys.append(3)  # Param is in position 3

    if grouping_keys:
        keys = np.array([tuple(col.split('_')[pos] for pos in grouping_keys) for col in ic_df.columns])
        unique_keys, inverse_indices = np.unique(keys, return_inverse=True, axis=0)

        grouped_averages = {}
        for i, unique_key in enumerate(unique_keys):
            mask = (inverse_indices == i)
            selected_columns = ic_df.columns[mask]
            mean_values = ic_df[selected_columns].mean(axis=1)
            grouped_averages['_'.join(unique_key)] = mean_values
    
        return pd.DataFrame(grouped_averages, index=ic_df.index, dtype=np.float32)

    return ic_df