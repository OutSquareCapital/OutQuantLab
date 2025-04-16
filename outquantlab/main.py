import numquant as nq
import tradeframe as tf
from outquantlab.backtest import Backtestor
from outquantlab.indicators import GenericIndic
from outquantlab.portfolio import (
    BacktestResults,
    get_categories_df,
    get_clusters,
)


class OutQuantLab:
    def __init__(self, indics: list[GenericIndic], returns_df: tf.FrameDated) -> None:
        self.indics: list[GenericIndic] = indics
        self.returns_df: tf.FrameDated = returns_df

    def backtest(self, local: bool = True) -> nq.Float2D:
        process = Backtestor(
            pct_returns=self.returns_df.get_array(), indics=self.indics, local=local
        )

        return process.process_backtest()

    def format_backtest(self, data: nq.Float2D) -> tf.FrameCategoricalDated:
        return tf.FrameCategoricalDated.create_from_np(
            data=data,
            dates=self.returns_df.index,
            categories=get_categories_df(
                asset_names=self.returns_df.get_names(), indics=self.indics
            ),
        )

    def get_portfolio(self, data: tf.FrameCategoricalDated) -> BacktestResults:
        return BacktestResults(params=data)

    def get_clusters(self, data: tf.FrameDated) -> dict[str, list[str]]:
        clean_df: tf.FrameDated = data.clean_nans(total=True)
        return get_clusters(
            returns_array=clean_df.get_array(), asset_names=clean_df.get_names(), max_clusters=5
        )