import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
import polars as pl


class FilesObject[T](ABC):
    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError


class FileHandler[T](ABC):
    _EXTENSION: str

    def __init__(self, db_path: Path, file_name: str) -> None:
        self.path: Path = db_path / f"{file_name}{self._EXTENSION}"

    def load(self, names: list[str] | None = None) -> T:
        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")
        return self._load_implementation(names=names)

    @abstractmethod
    def _load_implementation(self, names: list[str] | None = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} path: \n {self.path}\n"


class JSONHandler[K, V](FileHandler[dict[K, V]]):
    _EXTENSION = ".json"

    def _load_implementation(self, names: list[str] | None = None) -> dict[K, V]:
        with open(self.path, "r") as file:
            data: dict[K, V] = json.load(file)
        return data

    def save(self, data: dict[K, V]) -> None:
        with open(self.path, "w") as file:
            json.dump(data, file, indent=3)


class ParquetHandler(FileHandler[pl.DataFrame]):
    _EXTENSION = ".parquet"

    def _load_implementation(self, names: list[str] | None = None) -> pl.DataFrame:
        if names:
            return pl.read_parquet(source=self.path, columns=names)
        return pl.read_parquet(source=self.path)

    def save(self, data: pl.DataFrame) -> None:
        data.write_parquet(file=self.path)
