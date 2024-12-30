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
BASE_DIR: Final[str] = os.path.dirname(__file__)
DATA_DIR: Final[str] = "Saved_Data"
MEDIAS_DIR: Final[str] = "Medias"
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
class DataFiles:
    directory: str
    file_name: str
    ext: str
    full_path = property(lambda self: get_full_path(db_file=self, ext=self.ext))

def get_dir_path(directory:str, base_directory:str = BASE_DIR) -> str:
    return os.path.join(base_directory, directory)

def get_full_path(db_file: DataFiles, ext: str) -> str:
    dir_path: str = get_dir_path(directory=db_file.directory)
    file_path: str =os.path.join(dir_path, f"{db_file.file_name}{db_file.ext}")
    return file_path

class DataBaseQueries:
    def __init__(self) -> None:
        self.assets_to_test: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='assets_to_test',
            ext=JSON_EXT
            )
        self.indics_params: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='indics_params',
            ext=JSON_EXT
            )
        self.indics_to_test: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='indics_to_test',
            ext=JSON_EXT
            )
        self.indics_clusters: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='indics_clusters',
            ext=JSON_EXT
            )
        self.assets_clusters: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='assets_clusters',
            ext=JSON_EXT
            )
        self.price_data: DataFiles = DataFiles(
            directory=DATA_DIR,
            file_name='price_data',
            ext=PARQUET_EXT
            )
        self.home_page: DataFiles = DataFiles(
            directory=MEDIAS_DIR,
            file_name='home_page',
            ext=WEBP_EXT
            )
        self.loading_page: DataFiles = DataFiles(
            directory=MEDIAS_DIR,
            file_name='loading_page',
            ext=PNG_EXT
            )
        self.dashboard_page: DataFiles = DataFiles(
            directory=MEDIAS_DIR,
            file_name='dashboard_page',
            ext=PNG_EXT
            )
        self.app_logo: DataFiles = DataFiles(
            directory=MEDIAS_DIR,
            file_name='app_logo',
            ext=PNG_EXT
            )

        self.validate_datafiles()

    def validate_datafiles(self) -> None:
        for attr_name, attr_value in self.__dict__.items():
            if isinstance(attr_value, DataFiles) and attr_value.file_name != attr_name:
                raise ValueError(
                    f"Inconsistent file_name: {attr_name} has file_name '{attr_value.file_name}'"
                )

    def load_png(self, db_file: DataFiles) -> bytes:
        with open(file=db_file.full_path, mode="rb") as file:
            return file.read()

    def load_json(self, db_file: DataFiles) -> dict[str, Any]:
        with open(file=db_file.full_path, mode="r") as file:
            return json.load(fp=file)

    def save_json(self, db_file: DataFiles, data: dict[str, Any], indent: int = 3) -> None:
        with open(file=db_file.full_path, mode="w") as file:
            json.dump(obj=data, fp=file, indent=indent)

    def load_pq(self, db_file: DataFiles) -> pd.DataFrame:
        return pd.read_parquet(path=db_file.full_path, engine="pyarrow")

    def save_pq(self, db_file: DataFiles, data: pd.DataFrame) -> None:
        data.to_parquet(path=db_file.full_path, engine="pyarrow", index=True)

    def load_asset_names(self, db_file: DataFiles) -> list[str]:
        parquet_file = pq.ParquetFile(source=db_file.full_path)
        schema_names: Any = parquet_file.schema.names # type: ignore
        if isinstance(schema_names, list):
            return [col for col in schema_names if  col != "Date"] # type: ignore
        else:
            raise ValueError("Schema Names Not Available")

    def load_prices(self, db_file: DataFiles, asset_names: list[str]) -> tuple[ArrayFloat, pd.DatetimeIndex]:
        columns_to_load: list[str] = ["Date"] + [name for name in asset_names]
        prices_df = DataFrameFloat(data=pd.read_parquet(
            path=db_file.full_path,
            engine="pyarrow",
            columns=columns_to_load
        ))
        pct_returns_array: ArrayFloat = pct_returns_np(prices_array=prices_df.nparray)
        return pct_returns_array, prices_df.dates

    def get_yahoo_finance_data(self, db_file: DataFiles, assets: list[str]) -> None:
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
            path=db_file.full_path,
            index=True,
            engine="pyarrow"
        )