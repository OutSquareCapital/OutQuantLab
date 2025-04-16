import tradeframe as tf
from dataclasses import dataclass, field


@dataclass(slots=True)
class BacktestResults:
    params: tf.FrameCategoricalDated
    indics: tf.FrameDated = field(init=False)
    assets: tf.FrameDated = field(init=False)
    portfolio: tf.SeriesDated = field(init=False)
    
    def __post_init__(self) -> None:
        indics_by_assets_df: tf.FrameCategoricalDated = self.params.get_portfolio(["assets", "indics"])
        assets_df: tf.FrameCategoricalDated = indics_by_assets_df.get_portfolio(["assets"])
        #assets_by_indics_df: tf.FrameCategoricalDated = self.params.get_portfolio(["indics"])
        self.portfolio = assets_df.get_overall_portfolio()
        self.indics = tf.FrameDated.create_from_categorical(data=indics_by_assets_df)
        self.assets = tf.FrameDated.create_from_categorical(data=assets_df)