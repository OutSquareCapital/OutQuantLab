import json
from dataclasses import dataclass, field
from typing import Any, Final, Protocol

from pandas import DataFrame, read_parquet

JSON: Final[str] = ".json"
PARQUET: Final[str] = ".parquet"


class FileHandler(Protocol):
    def load(self, path: str, names: list[str] | None = None) -> Any:
        raise NotImplementedError

    def save(self, path: str, data: Any) -> None:
        raise NotImplementedError


class JSONHandler(FileHandler):
    def load(self, path: str, names: list[str] | None = None) -> dict[str, Any]:
        with open(path, "r") as file:
            data = json.load(file)
        if names:
            return {key: data[key] for key in names if key in data}
        return data

    def save(self, path: str, data: dict[str, Any]) -> None:
        with open(path, "w") as file:
            json.dump(data, file, indent=3)


class ParquetHandler(FileHandler):
    def load(self, path: str, names: list[str] | None = None) -> DataFrame:
        if names:
            return read_parquet(path, engine="pyarrow", columns=names)
        return read_parquet(path, engine="pyarrow")

    def save(self, path: str, data: DataFrame) -> None:
        data.to_parquet(path, engine="pyarrow", index=True)


def create_handler(ext: str) -> FileHandler:
    if ext == JSON:
        return JSONHandler()
    elif ext == PARQUET:
        return ParquetHandler()
    else:
        raise ValueError(f"Unsupported extension: {ext}")


@dataclass(frozen=True, slots=True)
class DataFile:
    ext: str
    path: str
    handler: FileHandler = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "handler", create_handler(self.ext))

    def load(self, names: list[str] | None = None) -> Any:
        return self.handler.load(path=self.path, names=names)

    def save(self, data: Any) -> None:
        self.handler.save(path=self.path, data=data)
