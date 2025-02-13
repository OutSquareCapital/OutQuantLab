import outquantlab.graphs as graphs
from outquantlab.backtest import execute_backtest
from outquantlab.config_classes import AppConfig
from outquantlab.database import DataBaseProvider
from outquantlab.typing_conventions import DataFrameFloat


class OutQuantLab:
    def __init__(self) -> None:
        self._dbp = DataBaseProvider()
        self.app_config: AppConfig = self._dbp.get_config()
        self.data: dict[str, DataFrameFloat] = {}
        self.graphs = graphs

    def run(self) -> None:
        self.data = execute_backtest(
            returns_df=self._dbp.get_data(
                names=self.app_config.assets_config.get_all_active_entities_names()
            ),
            backtest_config=self.app_config.get_backtest_config(),
        )

    def save(self) -> None:
        self._dbp.save_config(config=self.app_config)
