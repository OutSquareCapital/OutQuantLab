from enum import StrEnum
import polars as pl
from typing import Protocol, Any
from dataclasses import dataclass, field
import numquant as nq


class Category(Protocol):
    asset: str
    indic: str
    param: str


class ColumnsIDs(StrEnum):
    INDEX = "Index"
    VALUES = "Values"
    NAMES = "Names"
    DATE = "Date"


@dataclass(slots=True)
class SeriesConfig:
    index_col: str
    index_type: pl.DataType
    values_col: str = field(init=False, default=ColumnsIDs.VALUES)
    values_type: pl.Float32 = field(init=False, default=pl.Float32())

    @property
    def schema(self) -> dict[str, Any]:
        return {
            self.index_col: self.index_type,
            self.values_col: self.values_type,
        }

    def get_index(self, data: list[str] | nq.Int1D) -> pl.Series:
        return pl.Series(name=self.index_col, values=data, dtype=self.index_type)

    def get_data(self, array: nq.Float2D) -> pl.Series:
        return pl.Series(
            name=self.values_col, values=array, dtype=self.values_type
        ).fill_nan(value=None)

    def create(self, data: pl.Series, index: pl.Series) -> pl.DataFrame:
        return pl.DataFrame(
            data={self.index_col: index, self.values_col: data},
            schema=self.schema,
        )


@dataclass(slots=True)
class FrameConfig:
    index_col: str
    index_type: pl.DataType
    values_type: pl.Float32 = field(init=False, default=pl.Float32())

    @property
    def schema(self) -> dict[str, Any]:
        return {self.index_col: self.index_type}

    def create_empty(self) -> pl.DataFrame:
        return pl.DataFrame(
            data={
                self.index_col: pl.Series(name=self.index_col, values=[]),
            }
        )

    def get_data(self, array: nq.Float2D, asset_names: list[str]) -> pl.DataFrame:
        return pl.from_numpy(data=array, orient="row", schema=asset_names).fill_nan(
            value=None
        )

    def get_index(self, data: list[str] | nq.Int1D) -> pl.Series:
        return pl.Series(
            name=self.index_col,
            values=data,
            dtype=self.index_type,
        )

    def create(self, values: pl.DataFrame, index: pl.Series) -> pl.DataFrame:
        return values.with_columns(index)