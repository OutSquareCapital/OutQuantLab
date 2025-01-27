from outquantlab.backtest import execute_backtest
from outquantlab.config_classes import ConfigState
from outquantlab.database import DataBaseProvider

from outquantlab.graphs import GraphsCollection
from outquantlab.typing_conventions import DataFrameFloat


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.config: ConfigState = self.dbp.get_config()

    def run(self) -> GraphsCollection:
        returns_df: DataFrameFloat = self.dbp.get_data(
            names=self.config.assets_collection.get_all_active_entities_names()
        )
        return execute_backtest(
            returns_df=returns_df,
            config=self.config,
        )

    def save(self) -> None:
        self.dbp.save_config(config=self.config)
