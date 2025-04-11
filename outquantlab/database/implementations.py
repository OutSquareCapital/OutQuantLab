from pathlib import Path

from outquantlab.core import AssetsConfig, IndicsConfig
from outquantlab.database.interfaces import FilesObject, JSONHandler, ParquetHandler
from outquantlab.frames import DatedFloat

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


class TickersData(FilesObject[DatedFloat]):
    def __init__(self, db_path: Path) -> None:
        self.returns = ParquetHandler(db_path=db_path, file_name="returns_data")

    def get(self, assets: list[str] | None = None) -> DatedFloat:
        return self.returns.load(names=assets)

    def save(self, data: DatedFloat) -> None:
        self.returns.save(data=data)
