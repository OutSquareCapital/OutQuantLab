import pandas as pd
from typing import List
import yfinance as yf

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

def load_prices(file_path: str, asset_names: List[str]) -> pd.DataFrame:
    columns_to_load = ["Date"] + [name for name in asset_names]

    return pd.read_parquet(
        file_path,
        engine="pyarrow",
        columns=columns_to_load
    )