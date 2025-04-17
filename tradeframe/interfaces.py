from abc import ABC, abstractmethod
from typing import Self

import polars as pl

import numquant as nq
from pathlib import Path
from tradeframe.types import FrameConfig
from tradeframe.constructor import TradeFrameConstructor

class _AbstractTradeFrame(TradeFrameConstructor):

    def get_array(self) -> nq.Float2D:
        return self.values.to_numpy()

    @property
    @abstractmethod
    def values(self) -> pl.DataFrame:
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

class BaseIndexedHorizontal(_AbstractTradeFrame, ABC):
    _CONFIG: FrameConfig

    @property
    def index(self) -> pl.Series:
        index_list: list[str] = self.values.columns
        return pl.Series(name=self._CONFIG.index_col, values=index_list)

class _BaseIndexedVertical(_AbstractTradeFrame, ABC):
    _CONFIG: FrameConfig

    @property
    def index(self) -> pl.Series:
        return self._data[self._CONFIG.index_col]

    @abstractmethod
    def sort_data(self, ascending: bool) -> Self:
        raise NotImplementedError

    def get_last_row_dict(self) -> dict[str, float]:
        data: dict[str, list[float]] = self._data[-1:].to_dict(as_series=False)
        return {key: value[0] for key, value in data.items()}

class Frame2D(_BaseIndexedVertical):
    @property
    def values(self) -> pl.DataFrame:
        return self._data.drop(self._CONFIG.index_col)

    @classmethod
    def create_as_empty(cls) -> Self:
        return cls._construct(data=cls._CONFIG.create_empty())

    def get_names(self) -> list[str]:
        return self.values.columns

    def sort_data(self, ascending: bool) -> Self:
        value_cols: list[str] = self.values.columns
        mean_values: pl.DataFrame = self.values.mean()
        sorted_cols: list[str] = sorted(
            value_cols, key=lambda col: mean_values[col][0], reverse=not ascending
        )

        sorted_data: pl.DataFrame = self._data.select(
            [self._CONFIG.index_col] + sorted_cols
        )

        return self.__class__._construct(sorted_data)

    def clean_nans(self, total: bool = False) -> Self:
        asset_cols: list[str] = self.get_names()
        if total:
            df: pl.DataFrame = self._data.drop_nulls(subset=asset_cols)
            return self.__class__(df)
        else:
            df = self._data.filter(
                ~pl.all_horizontal(pl.col(name=asset_cols).is_null())
            )
            return self.__class__._construct(df)

