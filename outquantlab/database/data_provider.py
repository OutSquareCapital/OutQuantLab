import outquantlab.config_classes as cfg
from outquantlab.database.data_queries import DataQueries
from outquantlab.database.data_refresher import get_yf_data
from outquantlab.typing_conventions import DataFrameFloat


class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def refresh_assets_data(self, assets: list[str]) -> None:
        prices_data, returns_data = get_yf_data(assets=assets)
        self.save_assets_data(prices_data=prices_data, returns_data=returns_data)

    def get_returns_data(self, names: list[str]) -> DataFrameFloat:
        return DataFrameFloat(data=self.dbq.returns_data.load(names=names))

    def get_app_config(self) -> cfg.AppConfig:
        return cfg.AppConfig(
            indics_config=cfg.IndicsConfig(
                indics_active=self.dbq.indics_active.load(),
                params_config=self.dbq.indics_params.load(),
            ),
            assets_config=cfg.AssetsConfig(
                assets_active=self.dbq.assets_active.load(),
            ),
            assets_clusters=cfg.AssetsClusters(
                clusters=self.dbq.assets_clusters.load(),
            ),
            indics_clusters=cfg.IndicsClusters(
                clusters=self.dbq.indics_clusters.load(),
            ),
        )

    def save_app_config(
        self,
        config: cfg.AppConfig,
    ) -> None:
        self.dbq.assets_active.save(data=config.assets_config.get_all_entities_dict())
        self.dbq.indics_active.save(data=config.indics_config.get_all_entities_dict())
        self.dbq.indics_params.save(data=config.indics_config.prepare_indic_params())
        self.dbq.assets_clusters.save(data=config.assets_clusters.clusters)
        self.dbq.indics_clusters.save(data=config.assets_clusters.clusters)

    def save_assets_data(
        self, prices_data: DataFrameFloat, returns_data: DataFrameFloat
    ) -> None:
        self.dbq.prices_data.save(data=prices_data)
        self.dbq.returns_data.save(data=returns_data)

    def save_backtest_results(
        self, results: dict[str, dict[str, dict[str, list[str]]]]
    ) -> None:
        self.dbq.backtest_results.save(data=results)
