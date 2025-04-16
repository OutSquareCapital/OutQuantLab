import numquant as nq
import tradeframe as tf
from outquantlab.backtest import Backtestor
from outquantlab.indicators import GenericIndic
from outquantlab.portfolio import (
    BacktestResults,
    get_categories_dict_wide,
    get_categories_list_long,
    get_clusters,
    get_categories_df_wide,
    get_categories_df_long,
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

    def format_backtest(self, data: nq.Float2D) -> tf.FrameCategorical:
        asset_names: list[str] = self.returns_df.get_names()
        categories_dict = get_categories_dict_wide(
            asset_names=asset_names,
            indics=self.indics,
        )
        return tf.FrameCategorical.create_from_np(
            data=data,
            categories_df=get_categories_df_wide(
                data=categories_dict,
                asset_names=asset_names,
                indic_names=[indic.name for indic in self.indics],
            ),
        )

    def format_backtest_long(self, data: nq.Float2D) -> tf.FrameCategoricalLong:
        asset_names: list[str] = self.returns_df.get_names()
        categories_list = get_categories_list_long(
            asset_names=asset_names, indics=self.indics
        )
        return tf.FrameCategoricalLong(
            data=get_categories_df_long(
                data=data,
                categories=categories_list,
                asset_names=asset_names,
                indic_names=[indic.name for indic in self.indics],
            )
        )

    def get_portfolio(self, data: tf.FrameCategorical) -> BacktestResults:
        return BacktestResults(benchmark=self.returns_df, global_result=data)

    def get_clusters(self, data: tf.FrameDated) -> dict[str, list[str]]:
        clean_df: tf.FrameDated = data.clean_nans(total=True)
        return get_clusters(
            returns_array=clean_df.get_array(),
            asset_names=clean_df.get_names(),
            max_clusters=5,
        )
