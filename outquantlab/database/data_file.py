import json
from abc import ABC, abstractmethod
from pandas import DataFrame, read_parquet
from typing import Any

class DataFile[T:dict[str, Any] | DataFrame](ABC):

    def __init__(self) -> None:
        self.path: str = "default"

    @abstractmethod
    def load(self, names: list[str] | None = None) -> T:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: T) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"


class JSONFile(DataFile[dict[str, Any]]):
    def load(self, names: list[str] | None = None) -> dict[str, Any]:
        with open(self.path, "r") as file:
            data = json.load(file)
        if names:
            return {key: data[key] for key in names if key in data}
        return data

    def save(self, data: dict[str, Any]) -> None:
        with open(self.path, "w") as file:
            json.dump(data, file, indent=3)


class ParquetFile(DataFile[DataFrame]):
    def load(self, names: list[str] | None = None) -> DataFrame:
        if names:
            return read_parquet(self.path, engine="pyarrow", columns=names)
        return read_parquet(self.path, engine="pyarrow")

    def save(self, data: DataFrame) -> None:
        data.to_parquet(self.path, engine="pyarrow", index=True)