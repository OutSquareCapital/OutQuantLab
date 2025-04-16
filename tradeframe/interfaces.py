from abc import ABC, abstractmethod
from typing import Self

import polars as pl

import numquant as nq
from pathlib import Path
from tradeframe.types import FrameConfig, SeriesConfig

class AbstractTradeFrame(ABC):
    def __init__(self, data: pl.DataFrame) -> None:
        self._data: pl.DataFrame = data

    def __repr__(self) -> str:
        return f"{self._data}"

    def get_array(self) -> nq.Float2D:
        return self.values.to_numpy()

    @property
    @abstractmethod
    def values(self) -> pl.DataFrame | pl.Series:
        raise NotImplementedError

    @property
    @abstractmethod
    def index(self) -> pl.Series:
        raise NotImplementedError

    @abstractmethod
    def get_names(self) -> list[str]:
        raise NotImplementedError

    def to_parquet(self, path: Path) -> None:
        self._data.write_parquet(file=path)

class BaseWideFrame[T: FrameConfig | SeriesConfig ](AbstractTradeFrame, ABC):
    _CONFIG: T

    @property
    def index(self) -> pl.Series:
        return self._data[self._CONFIG.index_col]

    @abstractmethod
    def sort_data(self, ascending: bool) -> Self:
        raise NotImplementedError

    def get_last_row_dict(self) -> dict[str, float]:
        data: dict[str, list[float]] = self._data[-1:].to_dict(as_series=False)
        return {key: value[0] for key, value in data.items()}