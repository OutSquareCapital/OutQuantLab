import polars as pl

import numquant as nq
from typing import Self

class FrameCategorical:
    def __init__(self, data: pl.DataFrame, categories: list[str]) -> None:
        self._data: pl.DataFrame = data
        self._categories: list[str] = categories

    @property
    def values(self) -> pl.DataFrame:
        return self._data.drop(self._categories)

    def get_names(self) -> list[str]:
        return (
            self._data.select(pl.concat_str(exprs=self._categories, separator="_"))
            .to_series()
            .to_list()
        )

    @classmethod
    def create_from_np(
        cls,
        data: nq.Float2D,
        categories_df: pl.DataFrame
    ) -> Self:
        returns: pl.DataFrame = pl.from_numpy(data=data, orient="col").fill_nan(
            value=None
        )
        concatened_data: pl.DataFrame = pl.concat(
            items=[categories_df, returns], how="horizontal"
        )
        categories_names: list[str] = categories_df.columns
        return cls(data=concatened_data, categories=categories_names)

    def get_portfolio(self, categories: list[str]) -> Self:
        return_cols: list[str] = self.values.columns
        lazy_grouped: pl.LazyFrame = (
            self._data.lazy()
            .group_by(categories)
            .agg(pl.col(name=return_cols).mean().cast(dtype=pl.Float32()))
        )
        df: pl.DataFrame = lazy_grouped.collect()
        return self.__class__(data=df, categories=categories)


class FrameCategoricalLong:
    def __init__(self, data: pl.DataFrame) -> None:
        self._data: pl.DataFrame = data