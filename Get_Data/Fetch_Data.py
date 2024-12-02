import pandas as pd
from typing import List, Tuple
import yfinance as yf
import pyarrow.parquet as pq

def get_yahoo_finance_data(assets: List[str], file_path: str) -> None:

    data:pd.DataFrame = yf.download(
                                    assets,
                                    interval="1d",
                                    auto_adjust=True,
                                    progress=False,
                                )

    adj_close_df = data['Close']
    
    adj_close_df.to_parquet(
                            file_path,
                            index=True,
                            engine="pyarrow"
                            )

    print(f"Yahoo Finance Data Updated")

def load_asset_names(file_path: str) -> List[str]:
    parquet_file = pq.ParquetFile(file_path)
    column_names = parquet_file.schema.names
    return [col for col in column_names if col != "Date"]

def load_prices(file_path: str, asset_names) -> pd.DataFrame:
    columns_to_load = ["Date"] + [name for name in asset_names]

    # Charger uniquement les colonnes nécessaires
    return pd.read_parquet(
        file_path,
        engine="pyarrow",
        columns=columns_to_load
    )