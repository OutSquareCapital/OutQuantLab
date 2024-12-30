from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth
from typing import Any
from Metrics import pct_returns_np
import yfinance as yf # type: ignore
import pandas as pd
import pyarrow.parquet as pq # type: ignore
import json
from Utilitary import JSON_EXT, PARQUET_EXT

def load_config_file(file_path: str) -> DictVariableDepth:
    with open(file=file_path, mode="r") as file:
        return json.load(fp=file)

def save_config_file(file_path: str, dict_to_save: DictVariableDepth, indent: int) -> None:
    with open(file=file_path, mode="w") as file:
        json.dump(obj=dict_to_save, fp=file, indent=indent)

def load_asset_names(file_path: str) -> list[str]:
    parquet_file = pq.ParquetFile(source=file_path)
    schema_names: Any = parquet_file.schema.names # type: ignore
    if isinstance(schema_names, list):
        return [col for col in schema_names if  col != "Date"] # type: ignore
    else:
        raise ValueError("Schema Names Not Available")

def get_yahoo_finance_data(assets: list[str], file_path: str) -> None:
    data: pd.DataFrame|None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
        )
    
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")

    close_prices: pd.DataFrame = data["Close"] # type: ignore
    close_prices.to_parquet(
        path=file_path,
        index=True,
        engine="pyarrow"
    )

def load_prices(asset_names: list[str], file_path: str) -> tuple[ArrayFloat, pd.DatetimeIndex]:

    columns_to_load: list[str] = ["Date"] + [name for name in asset_names]

    prices_df = DataFrameFloat(data=pd.read_parquet(
        path=file_path,
        engine="pyarrow",
        columns=columns_to_load
    ))
    
    pct_returns_array: ArrayFloat = pct_returns_np(prices_array=prices_df.nparray)

    return pct_returns_array, prices_df.dates

class JSONFiles:
    @staticmethod
    def load(file_path: str) -> dict[str, Any]:
        if not file_path.endswith(JSON_EXT):
            raise ValueError(f"File must have {JSON_EXT} extension.")
        with open(file=file_path, mode="r") as file:
            return json.load(fp=file)

    @staticmethod
    def save(file_path: str, data: dict[str, Any], indent: int = 4) -> None:
        if not file_path.endswith(JSON_EXT):
            raise ValueError(f"File must have {JSON_EXT} extension.")
        with open(file=file_path, mode="w") as file:
            json.dump(obj=data, fp=file, indent=indent)

class ParquetFiles:
    @staticmethod
    def load(file_path: str) -> pd.DataFrame:
        if not file_path.endswith(PARQUET_EXT):
            raise ValueError(f"File must have {PARQUET_EXT} extension.")
        return pd.read_parquet(path=file_path, engine="pyarrow")

    @staticmethod
    def save(file_path: str, data: pd.DataFrame) -> None:
        if not file_path.endswith(PARQUET_EXT):
            raise ValueError(f"File must have {PARQUET_EXT} extension.")
        data.to_parquet(path=file_path, engine="pyarrow", index=True)