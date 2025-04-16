from pathlib import Path

import polars as pl
from pandas import DataFrame

import numquant as nq
from tradeframe.categorical import FrameCategoricalDated
from tradeframe.interfaces import BaseWideFrame
from tradeframe.types import ColumnsIDs, FrameConfig
from typing import Self


class Frame2D(BaseWideFrame[FrameConfig]):
    @classmethod
    def create_from_frames(cls, data: pl.DataFrame, index: pl.Series) -> Self:
        return cls(cls._CONFIG.create(values=data, index=index))

    @property
    def values(self) -> pl.DataFrame:
        return self._data.drop(self._CONFIG.index_col)

    @classmethod
    def create_as_empty(cls) -> Self:
        return cls(data=cls._CONFIG.create_empty())

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

        return self.__class__(sorted_data)

    def clean_nans(self, total: bool = False) -> Self:
        asset_cols: list[str] = self.get_names()
        if total:
            df: pl.DataFrame = self._data.drop_nulls(subset=asset_cols)
            return self.__class__(df)
        else:
            df = self._data.filter(
                ~pl.all_horizontal(pl.col(name=asset_cols).is_null())
            )
            return self.__class__(df)


class FrameDefault(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> "FrameDefault":
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )
        idx: nq.Int1D = nq.arrays.get_index(array=data)
        index: pl.Series = cls._CONFIG.get_index(data=idx)
        return cls.create_from_frames(data=returns, index=index)


class FrameDated(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.DATE, index_type=pl.Date())

    @classmethod
    def create_from_np(
        cls, data: nq.Float2D, asset_names: list[str], dates: pl.Series
    ) -> "FrameDated":
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )

        return cls.create_from_frames(data=returns, index=dates)

    @classmethod
    def create_from_parquet(
        cls, path: Path, names: list[str] | None = None
    ) -> "FrameDated":
        if names:
            columns_to_get: list[str] = [cls._CONFIG.index_col] + names
            df: pl.DataFrame = pl.read_parquet(source=path, columns=columns_to_get)
        else:
            df: pl.DataFrame = pl.read_parquet(source=path)
        return cls(
            data=df.with_columns(
                pl.col(name=cls._CONFIG.index_col).cast(dtype=cls._CONFIG.index_type)
            )
        )

    @classmethod
    def create_from_pd(cls, pd_df: DataFrame) -> "FrameDated":
        df: pl.DataFrame = pl.from_pandas(
            data=pd_df,
            include_index=True,
            schema_overrides=cls._CONFIG.schema,
        )
        return cls(
            data=df.with_columns(
                pl.col(name=cls._CONFIG.index_col).cast(dtype=cls._CONFIG.index_type)
            )
        )

    @classmethod
    def create_from_categorical(cls, data: FrameCategoricalDated) -> "FrameDated":
        transposed_data: pl.DataFrame = data.values.transpose(
            column_names=data.get_names()
        ).with_columns(data.index)
        return cls(data=transposed_data)


class FrameMatrix(Frame2D):
    _CONFIG = FrameConfig(index_col=ColumnsIDs.INDEX, index_type=pl.UInt32())

    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> "FrameMatrix":
        returns: pl.DataFrame = cls._CONFIG.get_data(
            array=data, asset_names=asset_names
        )
        index: pl.Series = cls._CONFIG.get_index(data=asset_names)
        return cls.create_from_frames(data=returns, index=index)
