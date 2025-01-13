import json
import os
import tempfile
from dataclasses import dataclass, field
from typing import Any, Final

import pandas as pd
import pyarrow.parquet as pq  # type: ignore

from Metrics import pct_returns_np
from Utilitary import APP_NAME, ArrayFloat, DataFrameFloat, FileHandler

JSON: Final[str] = ".json"
PARQUET: Final[str] = ".parquet"
PNG: Final[str] = ".png"
HTML: Final[str] = ".html"
FIG_TEMP_FILES: Final[str] = f"{APP_NAME}{HTML}"
HTML_ENCODING: Final[str] = "utf-8"


class HTMLHandler:
    def __init__(self) -> None:
        self.path_file: str = tempfile.mkstemp(suffix=HTML)[1]

    def load(self) -> str:
        with open(file=self.path_file, mode="w", encoding=HTML_ENCODING) as f:
            return f.read()

    def save(self, data: Any) -> None:
        with open(file=self.path_file, mode="w", encoding=HTML_ENCODING) as f:
            f.write(data)

    def cleanup_temp_files(self) -> None:
        try:
            os.remove(self.path_file)
        except Exception as e:
            raise Exception(
                f"Erreur lors de la suppression du fichier temporaire {self.path_file} : {e}"
            )


def create_handler(ext: str) -> FileHandler:
    if ext == JSON:
        return JSONHandler()
    elif ext == PARQUET:
        return ParquetHandler()
    elif ext == PNG:
        return PNGHandler()
    else:
        raise ValueError(f"Unsupported extension: {ext}")


class JSONHandler(FileHandler):
    def load(self, path: str) -> dict[str, Any]:
        with open(path, "r") as file:
            return json.load(file)

    def save(self, path: str, data: dict[str, Any]) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=3)


class ParquetHandler(FileHandler):
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_parquet(path, engine="pyarrow")

    def save(self, path: str, data: pd.DataFrame) -> None:
        data.to_parquet(path, engine="pyarrow", index=True)


class PNGHandler(FileHandler):
    def load(self, path: str) -> None:
        pass

    def save(self, path: str, data: Any) -> None:
        pass


@dataclass(frozen=True)
class DataFile:
    ext: str
    path: str
    handler: FileHandler = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "handler", create_handler(self.ext))

    def load(self) -> Any:
        return self.handler.load(path=self.path)

    def save(self, data: Any) -> None:
        self.handler.save(path=self.path, data=data)

    def load_asset_names(self) -> list[str]:
        parquet_file = pq.ParquetFile(self.path)

        columns: Any = parquet_file.schema.names  # type: ignore

        if "Date" in columns:
            columns.remove("Date")

        return columns

    def load_returns(self, asset_names: list[str]) -> ArrayFloat:
        columns_to_load: list[str] = [name for name in asset_names]
        prices_df = DataFrameFloat(
            data=pd.read_parquet(
                path=self.path, engine="pyarrow", columns=columns_to_load
            )
        )
        return pct_returns_np(prices_array=prices_df.nparray)

    def load_initial_data(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=pd.read_parquet(
                path=self.path, engine="pyarrow", columns=["Date", "SPY"]
            )
        )
