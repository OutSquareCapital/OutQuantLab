import polars as pl

import numquant as nq
from tradeframe.frames1d import SeriesDated
from tradeframe.types import ColumnsIDs, Category
from tradeframe.interfaces import AbstractTradeFrame
from typing import Self

class FrameCategoricalDated(AbstractTradeFrame):
    def __init__(self, data: pl.DataFrame, categories: list[str]) -> None:
        super().__init__(data=data)
        self._categories: list[str] = categories

    @property
    def values(self) -> pl.DataFrame:
        return self._data.drop(self._categories)

    @property
    def index(self) -> pl.Series:
        cols: list[str] = self.values.columns
        return pl.Series(name=ColumnsIDs.DATE, values=cols).cast(dtype=pl.Date)


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
        dates: pl.Series,
        categories: pl.DataFrame,
    ) -> "FrameCategoricalDated":
        returns: pl.DataFrame = pl.from_numpy(data=data, orient="col", schema=dates.to_list()).fill_nan(value=None)
        concatened_data: pl.DataFrame = pl.concat(items=[categories, returns], how="horizontal")
        categories_names: list[str] = categories.columns
        return cls(data=concatened_data, categories=categories_names)

    def get_portfolio(self, categories: list[str]) -> Self:
        return_cols: list[str] = self.values.columns
        lazy_grouped: pl.LazyFrame = (
            self._data.lazy()
            .group_by(categories)
            .agg(pl.col(name=return_cols).mean().cast(dtype=pl.Float32))
        )
        df: pl.DataFrame = lazy_grouped.collect()
        return self.__class__(data=df, categories=categories)

    def get_overall_portfolio(self) -> SeriesDated:
        data: pl.Series = self.values.select(pl.all().mean()).transpose().to_series()
        return SeriesDated.create_from_series(data=data, index=self.index)


# TODO: a terme, transferer la pipeline vers format long.
# sera nécessaire pour rolling correlation (dynamic groupby), sera bien mieux pour query le result via duckdb.
def format_backtest_long(
    data: nq.Float2D, dates: list[str], categories: list[Category]
) -> pl.DataFrame:
    """
        filter example to get a specific param of a specific indic of a specific asset:
        df.filter(
        (df["asset"] == "CORN") &
        (df["indic"] == "MeanPriceRatio") &
        (df["param"] == "4_16")
    )
    """
    n_dates: int = data.shape[0]
    result_frames: list[pl.DataFrame] = []

    for i, cat in enumerate(iterable=categories):
        df = pl.DataFrame(
            data={
                ColumnsIDs.DATE: pl.Series(name=ColumnsIDs.DATE, values=dates),
                "return": pl.Series(name="return", values=data[:, i], dtype=pl.Float32),
                "asset": pl.Series(name="asset", values=[cat.asset] * n_dates),
                "indic": pl.Series(name="indic", values=[cat.indic] * n_dates),
                "param": pl.Series(name="param", values=[cat.param] * n_dates),
            }
        )
        result_frames.append(df)

    return pl.concat(result_frames, rechunk=True)