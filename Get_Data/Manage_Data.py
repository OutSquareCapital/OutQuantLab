import os
from datetime import datetime
import pandas as pd

def convert_txt_to_csv(base_dir: str, output_base_dir: str):

    os.makedirs(output_base_dir, exist_ok=True)

    for subdir, _, files in os.walk(base_dir):
        if subdir == base_dir:
            continue

        subfolder_name = os.path.basename(subdir).upper()
        output_dir = os.path.join(output_base_dir, subfolder_name)
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(subdir, file)
                data_df = pd.read_csv(file_path, header=0 if pd.read_csv(file_path, nrows=0).shape[1] == 7 else None)

                if data_df.shape[1] < 7:
                    print(f"Avertissement : le fichier {file_path} a moins de 7 colonnes valides.")
                    continue
                
                if data_df.shape[1] == 7:
                    data_df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "OpenInt"]

                def parse_date(date_str):
                    try:
                        year_prefix = '19' if int(date_str[:2]) >= 40 else '20'
                        return datetime.strptime(year_prefix + date_str, '%Y%m%d').strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                        except ValueError:
                            return pd.NaT

                data_df["Date"] = data_df["Date"].astype(str).apply(parse_date)

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