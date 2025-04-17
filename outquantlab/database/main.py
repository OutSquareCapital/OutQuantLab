from outquantlab.core import AppConfig, AssetsConfig
from outquantlab.database.structure import DBStructure
import tradeframe as tf
from outquantlab.apis import YahooData


class DataBaseProvider:
    def __init__(self, db_name: str) -> None:
        self._db = DBStructure(name=db_name)
        self._yf = YahooData()

    def get_returns_data(
        self, config: AssetsConfig, new_data: bool
    ) -> tf.FrameDated:
        if new_data:
            data: tf.FrameDated = self._db.tickers.get()
            config.update_assets(names=data.get_names())
            self._db.assets.save(data=config)
            return data
        return self._db.tickers.get(
            assets=config.get_all_active_entities_names()
        )
    
    def refresh_data(self, config: AssetsConfig) -> None:
        assets: list[str] = config.get_all_entities_names()
        data: tf.FrameDated = self._yf.fetch_data(assets=assets)
        self._db.tickers.save(data=data)

    def get_app_config(self) -> AppConfig:
        return AppConfig(
            assets_config=self._db.assets.get(),
            indics_config=self._db.indics.get(),
        )

    def save_app_config(self, app_config: AppConfig) -> None:
        self._db.assets.save(data=app_config.assets_config)
        self._db.indics.save(data=app_config.indics_config)