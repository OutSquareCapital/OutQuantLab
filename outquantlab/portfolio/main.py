import tradeframe as tf


class BacktestResults:
    def __init__(
        self, benchmark: tf.FrameDefault, global_result: tf.FrameCategorical
    ) -> None:
        indics_by_assets_df: tf.FrameCategorical = global_result.get_portfolio(
            categories=["assets", "indics"]
        )
        assets_df: tf.FrameCategorical = indics_by_assets_df.get_portfolio(["assets"])
        self.indics: tf.FrameDefault = tf.FrameDefault.create_from_categorical(
            data=indics_by_assets_df
        )
        self.assets: tf.FrameDefault = tf.FrameDefault.create_from_categorical(
            data=assets_df
        )
