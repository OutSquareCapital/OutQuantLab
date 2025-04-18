import tradeframe as tf
from outquantlab.portfolio import get_clusters
from outquantlab.backtest import RawResults

class PortfolioConstructor:
    def __init__(
        self, data: RawResults
    ) -> None:
        global_result: tf.FrameCategoricalHorizontal = tf.FrameCategoricalHorizontal.create_from_np(
            data=data.array, categories_df=data.get_strategies_names_df()
        )
        indics_by_assets_df: tf.FrameCategoricalHorizontal = global_result.get_portfolio(
            categories=["asset", "indic"]
        )
        assets_df: tf.FrameCategoricalHorizontal = indics_by_assets_df.get_portfolio(categories=["asset"])
        self.indics: tf.FrameVertical = tf.FrameVertical.create_from_categorical_horizontal(
            data=indics_by_assets_df
        )
        self.assets: tf.FrameVertical = tf.FrameVertical.create_from_categorical_horizontal(
            data=assets_df
        )

    def get_clusters(self, data: tf.FrameVertical) -> dict[str, list[str]]:
        clean_df: tf.FrameVertical = data.clean_nans(total=True)
        return get_clusters(
            returns_array=clean_df.get_array(),
            asset_names=clean_df.get_names(),
            max_clusters=5,
        )
