from outquantlab.backtest import BacktestResults, execute_backtest
from outquantlab.config_classes import AppConfig
from outquantlab.database import DataBaseProvider
from outquantlab.local_ploty import Plots
from outquantlab.stats import StatsProvider


class OutQuantLab:
    def __init__(self, local: bool = True) -> None:
        self._dbp = DataBaseProvider()
        self.app_config: AppConfig = self._dbp.get_app_config()
        self.stats = StatsProvider()
        self.data: BacktestResults
        if local:
            self.plots = Plots()

    def run(self) -> None:
        self.data = execute_backtest(
            returns_df=self._dbp.get_returns_data(
                names=self.app_config.assets_config.get_all_active_entities_names()
            ),
            backtest_config=self.app_config.get_backtest_config(),
        )

    def save_results(self) -> None:
        portfolio_curves: dict[str, dict[str, list[str]]] = (
            self.stats.equity_curves.get_data(
                returns_df=self.data["portfolio"],  # type: ignore
                length=2500,
            ).convert_to_json(title=self.stats.equity_curves.title)
        )
        assets_sharpes: dict[str, dict[str, list[str]]] = (
            self.stats.overall_sharpe.get_data(
                returns_df=self.data["assets"]  # type: ignore
            ).convert_to_json(title=self.stats.overall_sharpe.title)
        )

        self._dbp.save_backtest_results(results=[portfolio_curves, assets_sharpes])

    def save_config(self) -> None:
        self._dbp.save_app_config(config=self.app_config)

    def check_data(self) -> None:
        for name, value in self.data.items():
            print(f"{name}:\n {value}")

    def refresh_data(self) -> None:
        self._dbp.refresh_assets_data(
            assets=self.app_config.assets_config.get_all_active_entities_names()
        )
