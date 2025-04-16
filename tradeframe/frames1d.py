from typing import Self

import polars as pl

import numquant as nq
from tradeframe.interfaces import Frame1D
from tradeframe.types import ColumnsIDs, SeriesConfig


class SeriesDefault(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D) -> Self:
        data_df: pl.Series = cls._CONFIG.get_data(array=data)
        idx: nq.Int1D = nq.arrays.get_index(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=idx)
        return cls._construct(cls._CONFIG.create(data=data_df, index=index))


class SeriesDated(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.DATE, index_type=pl.Date())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, index: pl.Series) -> Self:
        data_df: pl.Series = cls._CONFIG.get_data(array=data)
        return cls._construct(cls._CONFIG.create(data=data_df, index=index))


class SeriesNamed(Frame1D):
    _CONFIG = SeriesConfig(index_col=ColumnsIDs.NAMES, index_type=pl.Utf8())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, names: list[str]) -> Self:
        data_df: pl.Series = cls._CONFIG.get_data(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=names)
        return cls._construct(cls._CONFIG.create(data=data_df, index=index))
