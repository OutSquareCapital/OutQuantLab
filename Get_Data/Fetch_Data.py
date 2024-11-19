import pandas as pd
import numpy as np
from typing import List, Tuple
import yfinance as yf

def get_yahoo_finance_data(assets:list, file_path:str) -> None:

    # Télécharger les données de clôture ajustées pour chaque ticker
    data = yf.download(assets, interval="1d", auto_adjust=True, progress=False)
    
    # Sélectionner seulement la colonne 'Adj Close'
    adj_close_df = data['Close']
    
    # Enregistrer les données dans un fichier CSV
    adj_close_df.to_csv(file_path, index=True)

    print(f"Yahoo Finance Data Updated")


@staticmethod
def load_prices_from_csv(file_path: str, dtype=np.float32) -> Tuple[pd.DataFrame, List[str]]:
    """
    Charge le fichier CSV combiné et extrait les données des actifs (prix) ainsi que les noms des actifs.

    Args:
        file_path (str): Le chemin vers le fichier CSV combiné.
        dtype (type): Type de données pour les prix.
    
    Returns:
        Tuple[pd.DataFrame, List[str]]: Un DataFrame contenant les prix des actifs
        et une liste des noms d'actifs.
    """
    # Charger le fichier CSV dans un DataFrame
    prices_df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date', dtype=dtype)

    # Extraire les noms des actifs (correspond aux noms des colonnes du DataFrame)
    asset_names = list(prices_df.columns)

    return prices_df, asset_names