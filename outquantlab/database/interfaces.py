import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import tradeframe as tf


class FilesObject[T](ABC):
    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError

class FileHandler[T](ABC):
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


class JSONHandler[K, V](FileHandler[dict[K, V]]):
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


class ParquetHandler(FileHandler[tf.FrameDated]):
    extension = ".parquet"

    def _load_implementation(self, names: list[str] | None = None) -> tf.FrameDated:
        if names:
            data: tf.FrameDated = tf.FrameDated.create_from_parquet(path=self.path, names=names)
            return data.clean_nans()
        return tf.FrameDated.create_from_parquet(path=self.path)

    def _handle_missing_file(self) -> tf.FrameDated:
        empty_df: tf.FrameDated = tf.FrameDated.create_as_empty()
        empty_df.to_parquet(path=self.path)
        return empty_df

    def save(self, data: tf.FrameDated) -> None:
        data.to_parquet(path=self.path)
