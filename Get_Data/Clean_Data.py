import pandas as pd
import numpy as np
import os
from datetime import datetime
from Get_Data.Fetch_Data import load_prices_from_csv
from Process_Data import equity_curves_calculs

def convert_txt_to_csv(base_dir: str, output_base_dir: str):

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
    dfs = [] 

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

def adjust_prices_for_negativity(prices_df: pd.DataFrame) -> pd.DataFrame:

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

def adjust_prices_for_nans(prices_df: pd.DataFrame) -> pd.DataFrame:

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

    return pd.DataFrame(equity_curves_calculs(returns_df.values),
                        index=returns_df.index,
                        columns=returns_df.columns,
                        dtype=np.float32)

def clean_and_process_prices(file_path: str) -> None:

    raw_prices_df, _ = load_prices_from_csv(file_path)

    value_level_adjusted_raw_prices_df = adjust_prices_for_negativity(raw_prices_df)

    processed_prices_df = adjust_prices_for_nans(value_level_adjusted_raw_prices_df)

    processed_prices_df.to_csv(file_path)


