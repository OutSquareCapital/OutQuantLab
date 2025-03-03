import json
from dataclasses import dataclass, field
from typing import Any, Protocol, TypeVar, cast
from outquantlab.database.data_structure import Extension
from pandas import DataFrame, read_parquet

T = TypeVar("T")


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


_HANDLER_REGISTRY = {
    Extension.JSON.value: JSONHandler,
    Extension.PARQUET.value: ParquetHandler,
}


def create_handler(ext: str) -> FileHandler:
    handler_class = _HANDLER_REGISTRY.get(ext)
    if handler_class is None:
        raise ValueError(f"Unsupported extension: {ext}")
    return handler_class()


@dataclass(frozen=True, slots=True)
class DataFile:
    ext: str
    path: str
    handler: FileHandler = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "handler", create_handler(self.ext))

    def load(self, default_value: T, names: list[str] | None = None) -> T:
        try:
            data: T = cast(T, self.handler.load(path=self.path, names=names))
            return data
        except Exception as e:
            print(f"Error loading {self.path}: {e}")
            return default_value

    def save(self, data: Any) -> None:
        try:
            self.handler.save(path=self.path, data=data)
        except Exception as e:
            print(f"Error saving {self.path}: {e}")

    @property
    def handler_name(self) -> str:
        return self.handler.__class__.__name__
