import pandas as pd
import numpy as np
import os
from datetime import datetime
from Get_Data.Fetch_Data import load_prices_from_csv
from Process_Data import equity_curves_calculs

def convert_txt_to_csv(base_dir: str, output_base_dir: str):
    """
    Parcourt chaque sous-dossier dans `base_dir`, lit tous les fichiers .txt,
    les convertit en .csv, et les sauvegarde dans un nouveau dossier `output_base_dir`
    avec des sous-dossiers aux mêmes noms (en majuscules).
    
    Parameters:
    - base_dir (str): Le chemin du dossier contenant les fichiers .txt
    - output_base_dir (str): Le chemin du dossier où les fichiers .csv seront sauvegardés
    """
    # Création du dossier d'output s'il n'existe pas
    os.makedirs(output_base_dir, exist_ok=True)

    # Parcourir chaque sous-dossier dans base_dir
    for subdir, _, files in os.walk(base_dir):
        if subdir == base_dir:
            continue

        subfolder_name = os.path.basename(subdir).upper()
        output_dir = os.path.join(output_base_dir, subfolder_name)
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            if file.endswith(".txt"):
                # Chargement des données avec ou sans en-têtes
                file_path = os.path.join(subdir, file)
                data_df = pd.read_csv(file_path, header=0 if pd.read_csv(file_path, nrows=0).shape[1] == 7 else None)

                # Vérification du nombre de colonnes
                if data_df.shape[1] < 7:
                    print(f"Avertissement : le fichier {file_path} a moins de 7 colonnes valides.")
                    continue
                
                # Ajouter en-têtes si absents
                if data_df.shape[1] == 7:
                    data_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"]

                # Fonction pour convertir les dates en format standard avec détection du siècle
                def parse_date(date_str):
                    try:
                        # Format YYMMDD avec ajustement dynamique du siècle
                        year_prefix = '19' if int(date_str[:2]) >= 40 else '20'
                        return datetime.strptime(year_prefix + date_str, '%Y%m%d').strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            # Format MM/DD/YYYY
                            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                        except ValueError:
                            return pd.NaT  # Date non parsable

                # Appliquer la conversion de date
                data_df["Date"] = data_df["Date"].astype(str).apply(parse_date)

                # Sauvegarder le fichier en format CSV sans modification de structure
                output_file_path = os.path.join(output_dir, file.replace(".txt", ".csv"))
                data_df.to_csv(output_file_path, index=False)

    print("Conversion terminée pour tous les fichiers.")


def combine_csv_files(output_folder, file_names, output_file) -> None:
    """
    Combine multiple CSV files, ensuring all dates match across assets.
    Save the combined CSV, and return a corresponding dataframe.
    
    Args:
        output_folder (str): Folder containing the CSV files.
        file_names (list of str): List of filenames to combine.
        output_file (str): The name of the final combined CSV.
    """
    dfs = []  # Créer une liste pour stocker les DataFrames temporairement

    for file_name in file_names:
        file_path = os.path.join(output_folder, f"{file_name}.csv")
        
        # Charger le fichier CSV
        df = pd.read_csv(file_path, parse_dates=['time'], index_col='time')
        df.index.rename('date', inplace=True)
        
        # Renommer la colonne 'close' avec le nom de l'actif
        df = df[['close']].rename(columns={'close': file_name})
        
        # Ajouter le DataFrame à la liste
        dfs.append(df)

    # Concaténer tous les DataFrames le long de l'axe des colonnes avec alignement sur l'index
    combined_df = pd.concat(dfs, axis=1, join='outer')

    # Sauvegarder le DataFrame combiné dans un fichier CSV
    combined_df.to_csv(os.path.join(output_folder, output_file))


@staticmethod
def random_fill(series: pd.Series) -> pd.Series:
    """
    Remplit les NaN dans une série en utilisant la moyenne de X rendements aléatoires tirés avec remplacement.

    Args:
        series (pd.Series): Série de rendements avec potentiels NaNs.
        num_samples (int): Nombre d'échantillons aléatoires à tirer pour chaque NaN (par défaut 5).

    Returns:
        pd.Series: Série avec les NaN remplis.
    """
    # Index des NaN dans la série
    nan_indices = series[series.isna()].index
    
    # Identifie les rendements non NaN
    non_nan_series = series.dropna()

    # Boucle sur chaque NaN pour le remplacer par un rendement aléatoire du même actif
    for idx in nan_indices:
        # Tirer X samples aléatoires parmi les rendements non NaN
        random_sample = non_nan_series.sample(n=1, replace=True)

        # Remplacer le NaN par la valeur échantillonnée
        series.at[idx] = random_sample

    return series


@staticmethod
def adjust_prices_for_negativity(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajuste les séries de prix pour qu'aucune valeur ne soit négative.
    Ajoute un ajustement basé sur 1% du minimum absolu si nécessaire.

    Args:
        prices_df (pd.DataFrame): Un DataFrame contenant les prix des actifs.
    
    Returns:
        pd.DataFrame: Un DataFrame ajusté où toutes les valeurs sont positives.
    """
    # Ajuster les séries de prix pour qu'aucune valeur ne soit négative
    min_prices = prices_df.min()
    adjustment = abs(min_prices) + (min_prices.abs().max() * 0.01)  # Ajustement basé sur 1% du min absolu max
    # Liste pour suivre les colonnes ajustées
    affected_columns = []

    # Appliquer l'ajustement et suivre les colonnes affectées
    prices_df = prices_df.apply(lambda col: col + adjustment[col.name] if col.min() <= 0 else col)
    
    # Identifier les colonnes affectées
    for col in prices_df.columns:
        if min_prices[col] <= 0:
            affected_columns.append(col)
    
    # Imprimer les colonnes affectées
    if affected_columns:
        print(f"Colonnes affectées par l'ajustement pour prix négatifs: {affected_columns}")
    else:
        print("Aucune colonne affectée par l'ajustement pour prix négatifs")

    return prices_df

@staticmethod
def adjust_prices_for_nans(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme les prix en pourcentage, applique le bootstrap sur les NaNs et reconstitue les prix.
    Imprime des statistiques sur les rendements.

    Args:
        prices_df (pd.DataFrame): Un DataFrame contenant les prix des actifs.
    
    Returns:
        pd.DataFrame: Un DataFrame des prix reconstruits après avoir traité les rendements.
    """
    # Calcul des rendements en pourcentage de prices_df
    returns_df = prices_df.pct_change(fill_method=None)

    # Appliquer le forward fill après le premier prix valide pour chaque colonne
    for col in returns_df.columns:
        # Remplir seulement après avoir trouvé le premier prix valide (forward fill après ce point)
        first_valid_index = returns_df[col].first_valid_index()
        if first_valid_index is not None:

            # Calculer le nombre de jours (différence entre le premier prix valide et la fin des données)
            num_days = len(returns_df.loc[first_valid_index:])
            
            # Avant de faire le ffill, compter les NaNs après le premier prix valide
            num_cells_filled_before = returns_df[col].loc[first_valid_index:].isna().sum()

            # Appliquer le bootstrap pour remplir les NaNs après le premier jour valide
            returns_df.loc[first_valid_index:, col] = random_fill(returns_df.loc[first_valid_index:, col])

            # Calculer les statistiques
            filled_pct = ((num_cells_filled_before / num_days) * 100).round(2) if num_days > 0 else 0
            absolute_max_returns = returns_df[col].abs().max() * 100
            absolute_median_returns = returns_df[col].abs().median() * 100
            # Trouver les dates associées au max des rendements
            max_returns_date = returns_df[col].idxmax().strftime('%Y-%m-%d')

            # Imprimer les statistiques
            print(
                f"Actif : {col}, "
                f"Nombre de cellules aberrantes : {num_cells_filled_before}, "
                f"Proportion d'aberrants: {filled_pct}%, "
                f"Max absolu des rendements : {absolute_max_returns:.2f}% (le {max_returns_date}), "
                f"Médiane absolue des rendements : {absolute_median_returns:.2f}%"
            )

    return equity_curves_calculs(returns_df)

@staticmethod
def clean_and_process_prices(file_path: str) -> None:

    # Charger le data brut
    raw_prices_df, _ = load_prices_from_csv(file_path, dtype=np.float32)

    # Ajuster les prix pour éviter les valeurs négatives
    value_level_adjusted_raw_prices_df = adjust_prices_for_negativity(raw_prices_df)

    # Traiter les rendements, appliquer le bootstrap et reconstituer les prix
    processed_prices_df = adjust_prices_for_nans(value_level_adjusted_raw_prices_df)

    # Sauvegarder le DataFrame final dans un fichier CSV
    processed_prices_df.to_csv(file_path)


