import polars as pl

import numquant as nq
import tradeframe as tf


class DatesIndexer:
    _DATE = "Date"
    _INDEX = "Index"

    def __init__(self, dates_df: pl.DataFrame) -> None:
        daily_index: nq.Int1D = nq.arrays.get_index(array=dates_df.to_numpy())
        index = pl.Series(name=self._INDEX, values=daily_index, dtype=pl.Int32())
        dates = pl.Series(
            name=self._DATE, values=dates_df.select(pl.col(self._DATE)), dtype=pl.Date()
        )
        self.data = pl.DataFrame(
            data={
                self._DATE: dates,
                self._INDEX: index,
            }
        )


class TickersData:
    def __init__(
        self, prices: pl.DataFrame, returns: pl.DataFrame, dates: pl.DataFrame
    ) -> None:
        self.dates = DatesIndexer(dates_df=dates)
        asset_names: list[str] = returns.columns
        prices_array: nq.Float2D = nq.arrays.convert(data=prices.to_numpy())
        self.prices: tf.FrameVertical = tf.FrameVertical.create_from_np(
            data=prices_array, asset_names=asset_names
        )
        returns_array: nq.Float2D = nq.arrays.convert(data=returns.to_numpy())

        self.returns: tf.FrameVertical = tf.FrameVertical.create_from_np(
            data=returns_array, asset_names=asset_names
        )
