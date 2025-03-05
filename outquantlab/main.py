import outquantlab.graphs as graphs
from outquantlab.backtest import BacktestResults, execute_backtest
from outquantlab.config_classes import AppConfig
from outquantlab.database import DataBaseProvider


class OutQuantLab:
    def __init__(self) -> None:
        self._dbp = DataBaseProvider()
        self.app_config: AppConfig = self._dbp.get_app_config()
        self.graphs = graphs

    def run(self) -> None:
        self.data: BacktestResults = execute_backtest(
            returns_df=self._dbp.get_returns_data(
                names=self.app_config.assets_config.get_all_active_entities_names()
            ),
            backtest_config=self.app_config.get_backtest_config(),
        )

    def save(self) -> None:
        self._dbp.save_app_config(config=self.app_config)

    def check_data(self) -> None:
        for name, value in self.data.items():
            print(f"{name}:\n {value}")

    def refresh_data(self) -> None:
        self._dbp.refresh_assets_data(
            assets=self.app_config.assets_config.get_all_active_entities_names()
        )
