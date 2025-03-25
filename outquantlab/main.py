from outquantlab.config_classes import AppConfig, BacktestResults
from outquantlab.backtest import process_backtest
from outquantlab.database import DataBaseProvider

# from outquantlab.local_ploty import Plots
from outquantlab.stats import StatsProvider


class OutQuantLab:
    def __init__(self, local: bool = True) -> None:
        self._dbp = DataBaseProvider()
        self.app_config: AppConfig = self._dbp.get_app_config()
        self.stats = StatsProvider()

    def run(self) -> BacktestResults:
        return process_backtest(
            returns_df=self._dbp.get_returns_data(
                names=self.app_config.assets_config.get_all_active_entities_names()
            ),
            config=self.app_config.get_backtest_config(),
        )

    def save_results(self, results: BacktestResults) -> None:
        results_dict: dict[str, dict[str, dict[str, list[str]]]] = {}
        results_dict['rolling_sharpe_portfolio'] = (
            self.stats.rolling_sharpe_ratio.get_data(
                returns_df=results.portfolio,
                length=2500,
            ).convert_to_json(title=self.stats.rolling_sharpe_ratio.title)
        )
        results_dict['overall_sharpe_assets'] = (
            self.stats.overall_sharpe.get_data(
                returns_df=results.assets
            ).convert_to_json(title=self.stats.overall_sharpe.title)
        )

        self._dbp.save_backtest_results(results=results_dict)

    def save_config(self) -> None:
        self._dbp.save_app_config(config=self.app_config)

    def refresh_data(self) -> None:
        self._dbp.refresh_assets_data(
            assets=self.app_config.assets_config.get_all_active_entities_names()
        )
