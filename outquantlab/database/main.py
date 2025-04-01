from pathlib import Path

from outquantlab.config_classes import AppConfig
from outquantlab.database.implementations import (
    AssetFiles,
    AssetsClustersFiles,
    IndicFiles,
    IndicsClustersFiles,
    TickersData,
)
from outquantlab.database.interfaces import JSONFile, ParquetFile
from outquantlab.structures import DataFrameFloat

class DataBaseProvider:
    def __init__(self, db_name: str) -> None:
        db_path: Path = self._get_db_path(db_name=db_name)
        self.assets = AssetFiles(
            active=JSONFile(db_path=db_path, file_name="assets_active"),
        )

        self.indics = IndicFiles(
            active=JSONFile(db_path=db_path, file_name="indics_active"),
            params=JSONFile(db_path=db_path, file_name="indics_params"),
        )
        self.tickers = TickersData(
            returns=ParquetFile(db_path=db_path, file_name="returns_data"),
        )
        self.assets_clusters = AssetsClustersFiles(
            clusters=JSONFile(db_path=db_path, file_name="assets_clusters"),
        )
        self.indics_clusters = IndicsClustersFiles(
            clusters=JSONFile(db_path=db_path, file_name="indics_clusters"),
        )

    def _get_db_path(self, db_name: str) -> Path:
        current_file_path: Path = Path(__file__).resolve()
        current_dir: Path = current_file_path.parent
        return current_dir / db_name

    def get_returns_data(self, app_config: AppConfig) -> DataFrameFloat:
        return self.tickers.get(
            assets=app_config.assets_config.get_all_active_entities_names()
        )

    def refresh_data(self, app_config: AppConfig) -> None:
        self.tickers.refresh(assets=app_config.assets_config.get_all_entities_names())

    def get_app_config(self) -> AppConfig:
        return AppConfig(
            assets_config=self.assets.get(),
            assets_clusters=self.assets_clusters.get(),
            indics_config=self.indics.get(),
            indics_clusters=self.indics_clusters.get(),
        )

    def save_app_config(self, app_config: AppConfig) -> None:
        self.assets.save(data=app_config.assets_config)
        self.indics.save(data=app_config.indics_config)
        self.assets_clusters.save(data=app_config.assets_clusters)
        self.indics_clusters.save(data=app_config.indics_clusters)
