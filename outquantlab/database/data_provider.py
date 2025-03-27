from outquantlab.config_classes import (
    AppConfig,
    AssetsClusters,
    AssetsConfig,
    IndicsClusters,
    IndicsConfig,
)
from outquantlab.database.data_queries import DataBase, get_db
from outquantlab.database.data_refresher import AssetsData, fetch_data
from outquantlab.typing_conventions import DataFrameFloat


class DataBaseProvider:
    def __init__(self) -> None:
        self.db: DataBase = get_db()

    def check_data(self) -> None:
        for data in self.db:
            print(data)

    def get_app_config(self) -> AppConfig:
        return AppConfig(
            assets_config=self._get_assets_config(),
            assets_clusters=self._get_assets_clusters(),
            indics_config=self._get_indics_config(),
            indics_clusters=self._get_indics_clusters(),
        )

    def refresh_assets_data(self, assets: list[str]) -> None:
        data: AssetsData = fetch_data(assets=assets)
        self.db.backtest.prices.save(data=data.prices)
        self.db.backtest.returns.save(data=data.returns)

    def get_returns_data(self, assets: list[str] | None = None) -> DataFrameFloat:
        return DataFrameFloat(data=self.db.backtest.returns.load(names=assets))

    def _get_indics_config(self) -> IndicsConfig:
        return IndicsConfig(
            indics_active=self.db.indics.active.load(),
            params_config=self.db.indics.params.load(),
        )

    def _get_indics_clusters(self) -> IndicsClusters:
        return IndicsClusters(
            clusters=self.db.indics.clusters.load(),
        )

    def _get_assets_config(self) -> AssetsConfig:
        return AssetsConfig(
            assets_active=self.db.assets.active.load(),
        )

    def _get_assets_clusters(self) -> AssetsClusters:
        return AssetsClusters(
            clusters=self.db.assets.clusters.load(),
        )

    def save_backtest_results(self, results: dict[str, dict[str, list[str]]]) -> None:
        self.db.backtest.results.save(data=results)

    def save_config(self, config: AppConfig) -> None:
        self.db.assets.active.save(data=config.assets_config.get_all_entities_dict())
        self.db.assets.clusters.save(data=config.assets_clusters.clusters)
        self.db.indics.active.save(data=config.indics_config.get_all_entities_dict())
        self.db.indics.params.save(data=config.indics_config.prepare_indic_params())
        self.db.indics.clusters.save(data=config.indics_clusters.clusters)
