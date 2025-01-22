from database import DataQueries
from metrics import pct_returns_np
from typing_conventions import DataFrameFloat
import pandas as pd
import yfinance as yf  # type: ignore


    
def refresh_yf_data(dbq: DataQueries, assets: list[str]) -> None:
    data: pd.DataFrame | None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")
    else:
        prices_data = DataFrameFloat(data=data["Close"])  # type: ignore

        returns_data = DataFrameFloat(
            data=pct_returns_np(prices_array=prices_data.nparray),
            columns=prices_data.columns,
            index=prices_data.dates,
        )
        
        assets_names: list[str] = prices_data.columns.to_list()

        dbq.select(file="price_data").save(data=prices_data)
        dbq.select(file="returns_data").save(data=returns_data)
        dbq.select(file="assets_names").save(data=assets_names)