from outquantlab.backtest import process_backtest, BacktestResults
from outquantlab.core import AppConfig
from outquantlab.database import DataBaseProvider
from outquantlab.stats import Stats
from outquantlab.structures import frames
from outquantlab.apis import start_server


class OutQuantLab:
    def __init__(self, refresh_data: bool = True, db_name: str = "data") -> None:
        self._dbp = DataBaseProvider(db_name=db_name)
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

    def send_results(self, results:frames.DatedFloat) -> None:
        self.stats.rolling.sharpe_ratio.send_to_api(data=results, length=1250)
        self.stats.overall.sharpe_ratio.send_to_api(data=results)
        self.stats.distribution.send_to_api(data=results, frequency=20)
        start_server()
