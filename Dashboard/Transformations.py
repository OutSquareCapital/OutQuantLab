import numpy as np
import pandas as pd
import re
import Dashboard.Computations as Computations
from collections import defaultdict

def sort_columns_by_metric(metric_series: pd.Series, ascending: bool = True) -> list:

    return metric_series.sort_values(ascending=ascending).index.tolist()

def convert_params_to_4d(daily_returns, params):

    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)

    # Initialiser un dictionnaire pour stocker les Sharpe ratios par combinaison de paramètres
    sharpe_dict = defaultdict(list)

    # Extraire les paramètres et les ratios de Sharpe à partir de l'index
    for index, row in sharpe_ratios_df.iterrows():
        param_values = extract_all_params_from_name(index, params)

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

def convert_params_to_3d(daily_returns:pd.DataFrame, param1, param2):
    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)

    # Initialiser un dictionnaire pour stocker les Sharpe ratios par (param1, param2)
    sharpe_dict = defaultdict(list)

    # Extraire les paramètres et les ratios de Sharpe à partir de l'index
    for index, row in sharpe_ratios_df.iterrows():
        # Extraire les deux paramètres principaux
        param1_value, param2_value = extract_params_from_name(index, param1, param2)

        # Si on trouve les deux valeurs de param1 et param2, on stocke le Sharpe ratio
        if param1_value is not None and param2_value is not None:
            sharpe_dict[(param1_value, param2_value)].append(row['Sharpe Ratio'])

    # Initialiser les listes pour les valeurs moyennes des Sharpe ratios
    x_vals = []
    y_vals = []
    z_vals = []

    # Calculer les moyennes des Sharpe ratios pour chaque combinaison (param1, param2)
    for (p1, p2), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(np.nanmean(sharpe_list))  # Moyenne des Sharpe ratios
    
    # Convertir les listes en arrays numpy
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)

    # Créer une grille régulière à partir des valeurs uniques de x_vals (X) et y_vals (Y)
    x_unique = np.unique(x_vals)
    y_unique = np.unique(y_vals)
    X, Y = np.meshgrid(x_unique, y_unique)

    # Créer une grille Z qui correspond à la surface des Sharpe ratios
    Z = np.full_like(X, np.nan, dtype=np.float32)

    # Remplir la grille Z avec les valeurs correspondantes des Sharpe ratios
    for i in range(len(x_vals)):
        x_idx = np.where(x_unique == x_vals[i])[0][0]
        y_idx = np.where(y_unique == y_vals[i])[0][0]
        Z[y_idx, x_idx] = z_vals[i]

    return X, Y, Z

def extract_params_from_name(name: str, param1: str, param2: str) -> tuple:

    # Create regex patterns for each parameter
    pattern1 = re.compile(f"{param1}(\\d+)")
    pattern2 = re.compile(f"{param2}(\\d+)")
    
    # Search for the parameters in the name
    match1 = pattern1.search(name)
    match2 = pattern2.search(name)
    
    # Extract the values if matches are found, otherwise return None
    param1_value = int(match1.group(1)) if match1 else None
    param2_value = int(match2.group(1)) if match2 else None
    
    return param1_value, param2_value

def extract_all_params_from_name(name: str, params: list) -> list:

    extracted_values = []
    for param in params:
        pattern = re.compile(f"{param}(\\d+)")
        match = pattern.search(name)
        extracted_values.append(int(match.group(1)) if match else None)
    
    return extracted_values

def prepare_sunburst_data(cluster_dict, parent_label="", labels=None, parents=None):

    if labels is None:
        labels = []  # Réinitialisation de la liste à chaque appel
    if parents is None:
        parents = []  # Réinitialisation de la liste à chaque appel
        
    for key, value in cluster_dict.items():
        current_label = parent_label + str(key) if parent_label else str(key)  # Construit le label courant
        if isinstance(value, dict):
            # Si c'est un sous-cluster, on continue la récursion
            prepare_sunburst_data(value, current_label, labels, parents)
        else:
            # Si on arrive à une liste d'actifs, on les ajoute comme feuilles
            for asset in value:
                labels.append(asset)
                parents.append(current_label)
        # Ajouter le cluster actuel comme nœud s'il a des enfants
        if parent_label:
            labels.append(current_label)
            parents.append(parent_label)
        else:
            labels.append(current_label)
            parents.append("")  # Root node has no parent
            
    return labels, parents