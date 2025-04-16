from pathlib import Path
from typing import Self

import polars as pl
from pandas import DataFrame

import numquant as nq
from tradeframe.categorical import FrameCategorical
from tradeframe.interfaces import Frame2D
from tradeframe.types import ColumnsIDs, FrameConfig


class FrameDefault(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> Self:
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )
        idx: nq.Int1D = nq.arrays.get_index(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=idx)
        return cls._construct(cls._CONFIG.create(values=returns, index=index))


class FrameDated(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.DATE, index_type=pl.Date())

    @classmethod
    def create_from_np(
        cls, data: nq.Float2D, asset_names: list[str], dates: pl.Series
    ) -> Self:
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )

        return cls._construct(cls._CONFIG.create(values=returns, index=dates))

    @classmethod
    def create_from_parquet(cls, path: Path, names: list[str] | None = None) -> Self:
        if names:
            columns_to_get: list[str] = names + [cls._CONFIG.index_col]
            df: pl.DataFrame = pl.read_parquet(source=path, columns=columns_to_get)
        else:
            df: pl.DataFrame = pl.read_parquet(source=path)

        return cls._construct(data=cls._CONFIG.format_index(data=df))

    @classmethod
    def create_from_pd(cls, pd_df: DataFrame) -> Self:
        df: pl.DataFrame = pl.from_pandas(data=pd_df, include_index=True)

        return cls._construct(data=cls._CONFIG.format_index(data=df))

    @classmethod
    def create_from_categorical(cls, data: FrameCategorical, index: pl.Series) -> Self:
        transposed_data: pl.DataFrame = data.values.transpose(
            column_names=data.get_names()
        )
        return cls._construct(
            data=cls._CONFIG.create(values=transposed_data, index=index)
        )


class FrameMatrix(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> Self:
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )
        index: pl.Series = cls._CONFIG.get_index(data=asset_names)
        return cls._construct(cls._CONFIG.create(values=returns, index=index))
