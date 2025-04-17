from pathlib import Path

import polars as pl

from outquantlab.core import AssetsConfig, IndicsConfig, TickersData
from outquantlab.database.interfaces import FilesObject, JSONHandler, ParquetHandler
from outquantlab.apis import YahooData

class AssetFiles(FilesObject[AssetsConfig]):
    def __init__(self, db_path: Path) -> None:
        self.active = JSONHandler[str, bool](db_path=db_path, file_name="assets_active")

    def get(self) -> AssetsConfig:
        return AssetsConfig(
            assets_active=self.active.load(),
        )

    def save(self, data: AssetsConfig) -> None:
        self.active.save(data=data.get_all_entities_dict())


class IndicFiles(FilesObject[IndicsConfig]):
    def __init__(self, db_path: Path) -> None:
        self.active = JSONHandler[str, bool](db_path=db_path, file_name="indics_active")
        self.params = JSONHandler[str, dict[str, list[int]]](
            db_path=db_path, file_name="indics_params"
        )

    def get(self) -> IndicsConfig:
        return IndicsConfig(
            indics_active=self.active.load(),
            params_config=self.params.load(),
        )

    def save(self, data: IndicsConfig) -> None:
        self.active.save(data=data.get_all_entities_dict())
        self.params.save(data=data.prepare_indic_params())


class TickersDataFiles(FilesObject[TickersData]):
    def __init__(self, db_path: Path) -> None:
        self.returns = ParquetHandler(db_path=db_path, file_name="returns_data")
        self.prices = ParquetHandler(db_path=db_path, file_name="prices_data")
        self.dates = ParquetHandler(db_path=db_path, file_name="dates_data")

    def get(self, assets: list[str] | None = None) -> TickersData:
        returns_df: pl.DataFrame = self.returns.load(names=assets)
        prices_df: pl.DataFrame = self.prices.load(names=assets)
        dates_df: pl.DataFrame = self.dates.load()
        return TickersData(
            dates=dates_df,
            prices=prices_df,
            returns=returns_df,
        )
    def save(self, data: TickersData) -> None:
        self.returns.save(data=data.returns)
        self.prices.save(data=data.prices)
        self.dates.save(data=data.dates.data)

    def refresh_data(
        self, api: YahooData, config: AssetsConfig
    ) -> TickersData:
        api.refresh_data(assets=config.get_all_entities_names())
        data = TickersData(
            dates=api.dates,
            prices=api.prices,
            returns=api.returns,
        )
        config.update_assets(names=api.prices.columns)
        self.save(data=data)
        return data
