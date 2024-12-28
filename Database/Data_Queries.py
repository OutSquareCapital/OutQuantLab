from Utilitary import ArrayFloat, DataFrameFloat
from Metrics import pct_returns_np
import yfinance as yf # type: ignore
import pandas as pd

def get_yahoo_finance_data(assets: list[str], file_path: str) -> None:

    data: pd.DataFrame|None = yf.download( # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if isinstance(data, DataFrameFloat):
        data['Close'].to_parquet( # type: ignore
            file_path,
            index=True,
            engine="pyarrow"
        )
    else:
        raise ValueError("Yahoo Finance Data Not Available")


def load_prices(asset_names: list[str], file_path: str) -> tuple[ArrayFloat, pd.DatetimeIndex]:

    columns_to_load = ["Date"] + [name for name in asset_names]

    prices_df = DataFrameFloat(pd.read_parquet(
        file_path,
        engine="pyarrow",
        columns=columns_to_load
    ))
    
    pct_returns_array = pct_returns_np(prices_df.nparray)

    return pct_returns_array, prices_df.dates
