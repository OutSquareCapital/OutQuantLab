import pandas as pd
import yfinance as yf

def get_yahoo_finance_data(assets: list[str], file_path: str) -> None:

    data: pd.DataFrame|None = yf.download(
                            tickers=assets,
                            interval="1d",
                            auto_adjust=True,
                            progress=False,
                        )
    
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")

    data['Close'].to_parquet(
        file_path,
        index=True,
        engine="pyarrow"
    )