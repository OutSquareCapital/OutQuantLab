import pandas as pd
from typing import List, Tuple
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

def load_prices_from_parquet(file_path: str) -> Tuple[pd.DataFrame, List[str]]:
    
    prices_df = pd.read_parquet(
        file_path,
        engine="pyarrow"
    )

    asset_names = list(prices_df.columns)

    return prices_df, asset_names