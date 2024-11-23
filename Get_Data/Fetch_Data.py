import pandas as pd
import numpy as np
from typing import List, Tuple
import yfinance as yf

def get_yahoo_finance_data(assets:list, file_path:str) -> None:

    data = yf.download(assets, 
                       interval="1d", 
                       auto_adjust=True, 
                       progress=False)

    adj_close_df = data['Close']
    
    adj_close_df.to_csv(file_path, 
                        index=True)

    print(f"Yahoo Finance Data Updated")

def load_prices_from_csv(file_path: str) -> Tuple[pd.DataFrame, List[str]]:

    prices_df = pd.read_csv(file_path, 
                            parse_dates=['Date'], 
                            index_col='Date', 
                            dtype=np.float32)

    asset_names = list(prices_df.columns)

    return prices_df, asset_names