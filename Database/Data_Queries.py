from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth
from Metrics import pct_returns_np
import yfinance as yf # type: ignore
import pandas as pd
import pyarrow.parquet as pq # type: ignore
import json

def load_config_file(file_path: str) -> DictVariableDepth:
    with open(file_path, "r") as file:
        return json.load(file)

def save_config_file(file_path: str, dict_to_save: DictVariableDepth, indent: int) -> None:
    with open(file_path, "w") as file:
        json.dump(dict_to_save, file, indent=indent)

def load_asset_names(file_path: str) -> list[str]:
    column_names: list[str] = pq.ParquetFile(file_path).schema.names # type: ignore
    return [col for col in column_names if col != "Date"]

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
