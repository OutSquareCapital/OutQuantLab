from abc import ABC, abstractmethod
from typing import Self

import polars as pl

import numquant as nq
from pathlib import Path
from tradeframe.types import FrameConfig, SeriesConfig
from tradeframe.constructor import TFConstructor

class _AbstractTradeFrame(TFConstructor):

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


class _BaseWideFrame[T: FrameConfig | SeriesConfig](_AbstractTradeFrame, ABC):
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


class Frame1D(_BaseWideFrame[SeriesConfig]):
    @property
    def values(self) -> pl.Series:
        return self._data[self._CONFIG.values_col]

    def get_names(self) -> list[str]:
        return self.index.to_list()

    def sort_data(self, ascending: bool) -> Self:
        return self.__class__._construct(
            data=self._data.sort(by=self._CONFIG.values_col, descending=not ascending)
        )

    def get_dict(self) -> dict[str, float]:
        return dict(
            self._data.select(
                self._CONFIG.index_col, self._CONFIG.values_col
            ).iter_rows()
        )

    def clean_nans(self, total: bool = False) -> Self:
        if total:
            df: pl.DataFrame = self._data.drop_nulls(subset=self._CONFIG.values_col)
            return self.__class__._construct(df)
        else:
            df = self._data.filter(
                ~pl.all_horizontal(pl.col(name=self._CONFIG.values_col).is_null())
            )
            return self.__class__._construct(df)




class Frame2D(_BaseWideFrame[FrameConfig]):
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

