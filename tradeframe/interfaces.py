from abc import ABC, abstractmethod
from typing import Self

import polars as pl

import numquant as nq
from tradeframe.constructor import TradeFrameConstructor
from tradeframe.categorical import FrameCategorical


class _AbstractTradeFrame(TradeFrameConstructor):
    @property
    @abstractmethod
    def values(self) -> pl.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_names(self) -> list[str]:
        raise NotImplementedError

    def get_array(self) -> nq.Float2D:
        return self.values.to_numpy()


class FrameDefaultHorizontal(_AbstractTradeFrame, ABC):
    _NAMES = "Names"

    @property
    def values(self) -> pl.DataFrame:
        return self._data.drop(self._NAMES)

    def get_names(self) -> list[str]:
        return self._data[self._NAMES].to_list()

    @classmethod
    def _create_values(cls, array: nq.Float2D) -> pl.DataFrame:
        return pl.from_numpy(data=array, orient="col").fill_nan(value=None)

    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> Self:
        returns: pl.DataFrame = cls._create_values(array=data)
        return cls._construct(
            data=returns.with_columns(
                pl.Series(name=cls._NAMES, values=asset_names, dtype=pl.Utf8)
            )
        )


class FrameDefault(_AbstractTradeFrame, ABC):
    @classmethod
    def create_from_np(cls, data: nq.Float2D, asset_names: list[str]) -> Self:
        returns: pl.DataFrame = cls._create_values(array=data, asset_names=asset_names)
        return cls._construct(data=returns)

    @classmethod
    def create_from_categorical(cls, data: FrameCategorical) -> Self:
        transposed_data: pl.DataFrame = data.values.transpose(
            column_names=data.get_names()
        )
        return cls._construct(data=transposed_data)

    @property
    def values(self) -> pl.DataFrame:
        return self._data

    def get_names(self) -> list[str]:
        return self.values.columns

    @classmethod
    def _create_values(cls, array: nq.Float2D, asset_names: list[str]) -> pl.DataFrame:
        return pl.from_numpy(data=array, orient="row", schema=asset_names).fill_nan(
            value=None
        )

    def get_last_row_dict(self) -> dict[str, float]:
        data: dict[str, list[float]] = self._data[-1:].to_dict(as_series=False)
        return {key: value[0] for key, value in data.items()}

    def sort_data(self, ascending: bool) -> Self:
        value_cols: list[str] = self.values.columns
        mean_values: pl.DataFrame = self.values.mean()
        sorted_cols: list[str] = sorted(
            value_cols, key=lambda col: mean_values[col][0], reverse=not ascending
        )

        sorted_data: pl.DataFrame = self._data.select(sorted_cols)

        return self.__class__._construct(data=sorted_data)

    def clean_nans(self, total: bool = False) -> Self:
        asset_cols: list[str] = self.get_names()
        if total:
            df: pl.DataFrame = self._data.drop_nulls(subset=asset_cols)
            return self.__class__._construct(df)
        else:
            df = self._data.filter(
                ~pl.all_horizontal(pl.col(name=asset_cols).is_null())
            )
            return self.__class__._construct(data=df)
