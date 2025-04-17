import polars as pl
import numquant as nq
import tradeframe as tf


class DatesIndexer:
    def __init__(self, dates: pl.DataFrame) -> None:
        daily_index: nq.Int1D = nq.arrays.get_index(array=dates.to_numpy())
        self.data = pl.DataFrame(
            data={
                "Date": pl.Series(name="Date", values=dates, dtype=pl.Date()),
                "Index": pl.Series(name="Index", values=daily_index, dtype=pl.Int32()),
            }
        )


class TickersData:
    def __init__(
        self, dates: pl.DataFrame, prices: pl.DataFrame, returns: pl.DataFrame
    ) -> None:
        self.dates = DatesIndexer(dates=dates)
        self.prices: pl.DataFrame = prices
        self.returns: pl.DataFrame = returns

    def get_returns_data(self) -> tf.FrameDefault:
        array: nq.Float2D = nq.arrays.convert(data=self.returns.to_numpy())
        asset_names: list[str] = self.returns.columns
        data: tf.FrameDefault = tf.FrameDefault.create_from_np(
            data=array, asset_names=asset_names
        )
        return data
