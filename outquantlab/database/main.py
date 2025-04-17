from pathlib import Path
from outquantlab.database.implementations import (
    AssetFiles,
    IndicFiles,
    TickersData,
    AssetsConfig
)
import tradeframe as tf


class DBStructure:
    def __init__(self, db_name: str) -> None:
        self.path: Path = self._get_db_path(db_name=db_name)
        self.assets = AssetFiles(db_path=self.path)
        self.indics = IndicFiles(db_path=self.path)
        self.tickers = TickersData(db_path=self.path)

    def _get_db_path(self, db_name: str) -> Path:
        current_file_path: Path = Path(__file__).resolve()
        current_dir: Path = current_file_path.parent
        return current_dir / db_name

    def get_returns_data(
        self, config: AssetsConfig, new_data: bool
    ) -> tf.FrameDated:
        if new_data:
            data: tf.FrameDated = self.tickers.get()
            config.update_assets(names=data.get_names())
            self.assets.save(data=config)
            return data
        return self.tickers.get(
            assets=config.get_all_active_entities_names()
        )