import polars as pl

import numquant as nq
from tradeframe.interfaces import BaseWideFrame
from tradeframe.types import ColumnsIDs, SeriesConfig
from typing import Self


class Frame1D(BaseWideFrame[SeriesConfig]):
    @classmethod
    def create_from_series(cls, data: pl.Series, index: pl.Series) -> Self:
        return cls(cls._CONFIG.create(data=data, index=index))

    @property
    def values(self) -> pl.Series:
        return self._data[self._CONFIG.values_col]

    def get_names(self) -> list[str]:
        return self.index.to_list()

    def sort_data(self, ascending: bool) -> Self:
        return self.__class__(
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
            return self.__class__(df)
        else:
            df = self._data.filter(
                ~pl.all_horizontal(pl.col(name=self._CONFIG.values_col).is_null())
            )
            return self.__class__(df)


class SeriesDefault(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D) -> "SeriesDefault":
        data_df: pl.Series = cls._CONFIG.get_data(array=data)
        idx: nq.Int1D = nq.arrays.get_index(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=idx)
        return cls.create_from_series(data=data_df, index=index)


class SeriesDated(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.DATE, index_type=pl.Date())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, index: pl.Series) -> Self:
        df_data: pl.Series = cls._CONFIG.get_data(array=data)
        return cls.create_from_series(data=df_data, index=index)


class SeriesNamed(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.NAMES, index_type=pl.Utf8())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, names: list[str]) -> Self:
        df_data: pl.Series = cls._CONFIG.get_data(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=names)
        return cls.create_from_series(data=df_data, index=index)
