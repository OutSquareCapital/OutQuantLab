from outquantlab.backtest import process_backtest
from outquantlab.config_classes import AppConfig, BacktestResults
from outquantlab.database import DataBaseProvider
from outquantlab.stats import Stats
from outquantlab.typing_conventions import DataFrameFloat
from outquantlab.web_api import start_server


class OutQuantLab:
    def __init__(self, refresh_data: bool = True) -> None:
        self._dbp = DataBaseProvider()
        self.app_config: AppConfig = self._dbp.get_app_config()
        self.stats: Stats = Stats()
        if refresh_data:
            self._dbp.refresh_data(app_config=self.app_config)

    def run(self) -> BacktestResults:
        return process_backtest(
            returns_df=self._dbp.get_returns_data(app_config=self.app_config),
            config=self.app_config.get_backtest_config(),
        )

    def save_config(self) -> None:
        self._dbp.save_app_config(app_config=self.app_config)

    def send_results(self, results: DataFrameFloat) -> None:
        self.stats.rolling.sharpe_ratio.send_to_api(data=results, length=1250)
        self.stats.overall.sharpe_ratio.send_to_api(data=results)
        self.stats.distribution.send_to_api(data=results, frequency=20)
        start_server()
