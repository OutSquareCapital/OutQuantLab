import os

from outquantlab.database.data_file import ParquetFile, JSONFile
from dataclasses import dataclass, field

DB_NAME = "data"


@dataclass
class DataQueries:
    assets_active: JSONFile = field(default_factory=JSONFile)
    assets_clusters: JSONFile = field(default_factory=JSONFile)
    indics_active: JSONFile = field(default_factory=JSONFile)
    indics_params: JSONFile = field(default_factory=JSONFile)
    indics_clusters: JSONFile = field(default_factory=JSONFile)
    returns_data: ParquetFile = field(default_factory=ParquetFile)
    prices_data: ParquetFile = field(default_factory=ParquetFile)
    backtest_results: JSONFile = field(default_factory=JSONFile)

    def __post_init__(self) -> None:
        current_file_path: str = os.path.abspath(__file__)
        current_dir: str = os.path.dirname(current_file_path)
        db_path: str = os.path.join(current_dir, DB_NAME)

        for root, _, files in os.walk(db_path):
            for file in files:
                file_path: str = os.path.join(root, file)
                file_name, _ = os.path.splitext(file)
                self._assign_path(path=file_path, file_name=file_name)

    def _assign_path(self, path: str, file_name: str) -> None:
        try:
            self[file_name].path = path
        except KeyError:
            raise ValueError(f"File {file_name} at \n {path} \n not found in DataQueries list")

    def check_data(self) -> None:
        for name, value in self.__dict__.items():
            print(f"{name}:\n {value}")

    def __getitem__(self, key: str) -> ParquetFile | JSONFile:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: ParquetFile | JSONFile) -> None:
        self.__dict__[key] = value
