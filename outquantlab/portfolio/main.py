import tradeframe as tf


class BacktestResults:
    def __init__(
        self, benchmark: tf.FrameDated, global_result: tf.FrameCategorical
    ) -> None:
        indics_by_assets_df: tf.FrameCategorical = global_result.get_portfolio(
            categories=["assets", "indics"]
        )
        assets_df: tf.FrameCategorical = indics_by_assets_df.get_portfolio(["assets"])
        self.indics: tf.FrameDated = tf.FrameDated.create_from_categorical(
            data=indics_by_assets_df, index=benchmark.index
        )
        self.assets: tf.FrameDated = tf.FrameDated.create_from_categorical(
            data=assets_df, index=benchmark.index
        )
