import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from dataclasses import dataclass

from outquantlab.structures import DatedDataFrameFloat

@dataclass
class FilesObject[T](ABC):
    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError

class DataFile[T](ABC):
    extension: str

    def __init__(self, db_path: Path, file_name: str) -> None:
        self.path: Path = db_path / f"{file_name}{self.extension}"

    def load(self, names: list[str] | None = None) -> T:
        if not self.path.exists():
            print(
                f"File {self.path.name} is not found. Returning empty data.\n{self.path}"
            )
            return self._handle_missing_file()
        return self._load_implementation(names=names)

    @abstractmethod
    def _load_implementation(self, names: list[str] | None = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def _handle_missing_file(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} path: \n {self.path}\n"


class JSONFile[K, V](DataFile[dict[K, V]]):
    extension = ".json"

    def _load_implementation(self, names: list[str] | None = None) -> dict[K, V]:
        with open(self.path, "r") as file:
            data: dict[K, V] = json.load(file)
        return data

    def _handle_missing_file(self) -> dict[K, V]:
        with open(self.path, "w") as file:
            json.dump({}, file, indent=3)
        return {}

    def save(self, data: dict[K, V]) -> None:
        with open(self.path, "w") as file:
            json.dump(data, file, indent=3)


class ParquetFile(DataFile[DatedDataFrameFloat]):
    extension = ".parquet"

    def _load_implementation(self, names: list[str] | None = None) -> DatedDataFrameFloat:
        if names:
            return DatedDataFrameFloat.from_parquet(path=self.path, names=names)
        return DatedDataFrameFloat.from_parquet(path=self.path)

    def _handle_missing_file(self) -> DatedDataFrameFloat:
        empty_df: DatedDataFrameFloat = DatedDataFrameFloat.as_empty()
        empty_df.to_parquet(self.path, engine="pyarrow", index=True)
        return empty_df

    def save(self, data:DatedDataFrameFloat) -> None:
        data.to_parquet(self.path, engine="pyarrow", index=True)
