from dataclasses import dataclass
from Utilitary import ArrayFloat, DataFrameFloat
from typing import Any, Final
from Metrics import pct_returns_np
import yfinance as yf # type: ignore
import pandas as pd
import pyarrow.parquet as pq # type: ignore
import json
import os
import tempfile

JSON_EXT: Final = ".json"
PARQUET_EXT: Final = ".parquet"
WEBP_EXT: Final = ".webp"
PNG_EXT: Final = ".png"
HTML_EXT: Final = ".html"
N_THREADS: Final = os.cpu_count() or 8
BASE_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")
TEMPFILES_DIR: Final[str] = tempfile.gettempdir()
FIG_TEMP_FILES: Final[str] = f"outquant{HTML_EXT}"
HTML_ENCODING: Final[str] = "utf-8"

def process_html_temp_file(html_content: Any, suffix: str = FIG_TEMP_FILES) -> str:
    temp_file= tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    save_html(file_path=temp_file.name, data=html_content)
    return temp_file.name

def save_html(file_path: str, data: Any) -> None:
    with open(file=file_path, mode='w', encoding=HTML_ENCODING) as f:
        f.write(data)

def cleanup_temp_files(temp_dir:str = TEMPFILES_DIR, suffix:str = FIG_TEMP_FILES) -> None:
    for file_name in os.listdir(path=temp_dir):
        if file_name.endswith(suffix):
            file_path: str = os.path.join(temp_dir, file_name)
            try:
                os.remove(path=file_path)
            except Exception as e:
                raise Exception(f"Erreur lors de la suppression du fichier temporaire {file_path} : {e}")

@dataclass(frozen=True)
class DataFile:
    ext: str
    full_path: str

    def load_json(self) -> dict[str, Any]:
        with open(file=self.full_path, mode="r") as file:
            return json.load(fp=file)

    def load_pq(self) -> pd.DataFrame:
        return pd.read_parquet(path=self.full_path, engine="pyarrow")

    def save_json(self, data: dict[str, Any], indent: int = 3) -> None:
        with open(file=self.full_path, mode="w") as file:
            json.dump(obj=data, fp=file, indent=indent)

    def save_pq(self, data: pd.DataFrame) -> None:
        data.to_parquet(path=self.full_path, engine="pyarrow", index=True)

    def load_asset_names(self) -> list[str]:
        parquet_file = pq.ParquetFile(source=self.full_path)
        schema_names: Any = parquet_file.schema.names # type: ignore
        if isinstance(schema_names, list):
            return [col for col in schema_names if  col != "Date"] # type: ignore
        else:
            raise ValueError("Schema Names Not Available")

    def load_prices(self, asset_names: list[str]) -> tuple[ArrayFloat, pd.DatetimeIndex]:
        columns_to_load: list[str] = ["Date"] + [name for name in asset_names]
        prices_df = DataFrameFloat(data=pd.read_parquet(
            path=self.full_path,
            engine="pyarrow",
            columns=columns_to_load
        ))
        pct_returns_array: ArrayFloat = pct_returns_np(prices_array=prices_df.nparray)
        return pct_returns_array, prices_df.dates

class DataBaseQueries:
    def __init__(self, base_dir: str = BASE_DIR) -> None:
        self.select: dict[str, DataFile] = {}
        self.__generate_datafiles(base_dir)

    def __generate_datafiles(self, base_dir: str = BASE_DIR) -> None:
        for root, _, files in os.walk(base_dir):
            for file_name in files:
                file_path: str = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    file_base, file_ext = os.path.splitext(file_name)
                    datafile = DataFile(
                        ext=file_ext,
                        full_path=file_path
                    )

                    self.select[file_base] = datafile

    def get_yahoo_finance_data(self, f: DataFile, assets: list[str]) -> pd.DataFrame:
        data: pd.DataFrame|None = yf.download(  # type: ignore
            tickers=assets,
            interval="1d",
            auto_adjust=True,
            progress=False,
            )
        if data is None:
            raise ValueError("Yahoo Finance Data Not Available")
        else:
            return DataFrameFloat(data=data["Close"]) # type: ignore