from outquantlab.core import AppConfig
from outquantlab.database.structure import DBStructure, get_db_structure
from outquantlab.structures import frames
from outquantlab.apis import fetch_data


class DataBaseProvider:
    def __init__(self, db_name: str) -> None:
        self._db: DBStructure = get_db_structure(db_name=db_name)

    def get_returns_data(
        self, app_config: AppConfig, new_data: bool
    ) -> frames.DatedFloat:
        if new_data:
            data: frames.DatedFloat = self._db.tickers.get()
            app_config.assets_config.update_assets(names=data.get_names())
            self._db.assets.save(data=app_config.assets_config)
            return data
        return self._db.tickers.get(
            assets=app_config.assets_config.get_all_active_entities_names()
        )

    def refresh_data(self, app_config: AppConfig) -> None:
        assets: list[str] = app_config.assets_config.get_all_entities_names()
        data: frames.DatedFloat = fetch_data(assets=assets)
        self._db.tickers.save(data=data)

    def get_app_config(self) -> AppConfig:
        return AppConfig(
            assets_config=self._db.assets.get(),
            indics_config=self._db.indics.get(),
        )

    def save_app_config(self, app_config: AppConfig) -> None:
        self._db.assets.save(data=app_config.assets_config)
        self._db.indics.save(data=app_config.indics_config)