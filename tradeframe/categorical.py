import polars as pl

import numquant as nq
from tradeframe.types import ColumnsIDs, Category
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
        categories: list[dict[str, str]],
        asset_names: list[str],
        indic_names: list[str],
    ) -> Self:
        categories_df: pl.DataFrame = cls.get_categories_schema(
            data=categories, asset_names=asset_names, indic_names=indic_names
        )
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

    @classmethod
    def get_categories_schema(
        cls, data: list[dict[str, str]], asset_names: list[str], indic_names: list[str]
    ) -> pl.DataFrame:
        assets_categories = pl.Enum(categories=asset_names)
        indics_categories = pl.Enum(categories=indic_names)
        schema = {
            "assets": assets_categories,
            "indics": indics_categories,
            "params": pl.Utf8,
        }
        return pl.DataFrame(data=data, schema=schema)


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


