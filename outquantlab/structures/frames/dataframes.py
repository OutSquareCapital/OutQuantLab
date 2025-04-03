from datetime import datetime
from pathlib import Path
from typing import TypedDict

from numpy import nanmean
from pandas import (
    DataFrame,
    DatetimeIndex,
    Index,
    MultiIndex,
    RangeIndex,
    read_parquet,
)

import outquantlab.structures.arrays as arrays


class DistributionDict(TypedDict):
    data: list[list[float]]
    columns: list[str]


class DatedDict(TypedDict):
    data: list[list[float]]
    index: list[datetime]
    columns: list[str]


class BaseFloat[T: DatetimeIndex | None](DataFrame):
    def __init__(
        self,
        data: arrays.Float2D | list[float],
        index: T,
        columns: list[str] | MultiIndex | Index,  # type: ignore
    ) -> None:
        super().__init__(data=data, index=index, columns=columns, dtype=arrays.Float32)  # type: ignore

    def select(self, column: str) -> list[float]:
        return self[column].tolist()  # type: ignore

    def clean_nans(self) -> None:
        self.dropna(axis=0, how="all", inplace=True)  # type: ignore

    def get_array(self) -> arrays.Float2D:
        return self.to_numpy(copy=False, na_value=arrays.Nan)  # type: ignore

    def get_names(self) -> list[str]:
        if isinstance(self.columns, MultiIndex):
            return ["_".join(col).replace(" ", "_") for col in self.columns.to_list()]
        return self.columns.to_list()


class DefaultFloat(BaseFloat[None]):
    def __init__(
        self,
        data: arrays.Float2D | list[float],
        columns: list[str] | MultiIndex | Index,  # type: ignore
    ) -> None:
        super().__init__(data=data, index=None, columns=columns)  # type: ignore

    def get_index(self) -> RangeIndex:
        return self.index  # type: ignore

    def sort_data(self, ascending: bool) -> "DefaultFloat":
        mean_values: arrays.Float2D = nanmean(self.get_array(), axis=0)
        sorted_indices: arrays.Int2D = arrays.get_sorted_indices(
            array=mean_values, ascending=ascending
        )

        sorted_data: arrays.Float2D = self.get_array()[:, sorted_indices]
        sorted_columns: list[str] = [self.columns[i] for i in sorted_indices]

        return DefaultFloat(data=sorted_data, columns=sorted_columns)

    def get_index_list(self) -> list[int]:
        return self.get_index().tolist()  # type: ignore

    def convert_to_json(self) -> DistributionDict:
        self.clean_nans()
        column_data: list[list[float]] = []
        for col_name in self.columns:
            values: list[float] = self.select(column=col_name)
            column_data.append(values)

        return DistributionDict(data=column_data, columns=self.get_names())


class DatedFloat(BaseFloat[DatetimeIndex]):
    def get_index(self) -> DatetimeIndex:
        return self.index  # type: ignore

    @classmethod
    def as_empty(cls) -> "DatedFloat":
        return cls(
            data=arrays.empty(shape=(0, 0)),
            index=DatetimeIndex(data=[datetime.now()]),
            columns=[],
        )

    @classmethod
    def from_pandas(cls, data: DataFrame) -> "DatedFloat":
        return cls(
            data=data.to_numpy(dtype=arrays.Float32, copy=False, na_value=arrays.Nan),  # type: ignore
            index=data.index,  # type: ignore
            columns=data.columns,
        )

    @classmethod
    def from_parquet(
        cls, path: Path, names: list[str] | None = None
    ) -> "DatedFloat":
        data: DataFrame = read_parquet(path, engine="pyarrow", columns=names)
        return cls.from_pandas(data=data)

    def sort_data(self, ascending: bool) -> "DatedFloat":
        mean_values: arrays.Float2D = nanmean(self.get_array(), axis=0)
        sorted_indices: arrays.Int2D = arrays.get_sorted_indices(
            array=mean_values, ascending=ascending
        )

        sorted_data: arrays.Float2D = self.get_array()[:, sorted_indices]
        sorted_columns: list[str] = [self.columns[i] for i in sorted_indices]

        return DatedFloat(
            data=sorted_data, columns=sorted_columns, index=self.get_index()
        )

    def get_index_list(self) -> list[datetime]:
        return self.get_index().to_pydatetime().tolist()

    def convert_to_json(self) -> DatedDict:
        self.clean_nans()
        column_data: list[list[float]] = []
        for col_name in self.columns:
            values: list[float] = self.select(column=col_name)
            column_data.append(values)

        return DatedDict(
            data=column_data,
            index=self.get_index_list(),
            columns=self.get_names(),
        )
