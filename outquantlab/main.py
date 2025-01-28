from outquantlab.backtest import execute_backtest
from outquantlab.config_classes import AppConfig
from outquantlab.database import DataBaseProvider
from outquantlab.graphs import GraphsCollection


class OutQuantLab:
    def __init__(self) -> None:
        self.dbp = DataBaseProvider()
        self.app_config: AppConfig = self.dbp.get_config()

    def run(self) -> GraphsCollection:
        return execute_backtest(
            data_dfs=self.dbp.get_data(
                names=self.app_config.assets_config.get_all_active_entities_names()
            ),
            backtest_config=self.app_config.get_backtest_config(),
        )

    def save(self) -> None:
        self.dbp.save_config(config=self.app_config)
