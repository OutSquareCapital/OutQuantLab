import os

import pandas as pd
import yfinance as yf  # type: ignore

from DataBase.Data_File import DataFile
from TypingConventions import DataFrameFloat

BASE_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")


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
                    datafile = DataFile(ext=file_ext, path=file_path)

                    self.select[file_base] = datafile

    @staticmethod
    def get_yahoo_finance_data(assets: list[str]) -> pd.DataFrame:
        data: pd.DataFrame | None = yf.download(  # type: ignore
            tickers=assets,
            interval="1d",
            auto_adjust=True,
            progress=False,
        )
        if data is None:
            raise ValueError("Yahoo Finance Data Not Available")
        else:
            return DataFrameFloat(data=data["Close"])  # type: ignore
