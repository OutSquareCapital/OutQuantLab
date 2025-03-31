from dataclasses import dataclass

from outquantlab.config_classes import (
    AssetsClusters,
    AssetsConfig,
    IndicsClusters,
    IndicsConfig,
)
from outquantlab.database.interfaces import FilesObject, JSONFile, ParquetFile
from outquantlab.typing_conventions import DataFrameFloat
from outquantlab.web_api import fetch_data


@dataclass
class AssetsClustersFiles(FilesObject[AssetsClusters]):
    clusters: JSONFile[str, dict[str, list[str]]]

    def get(self) -> AssetsClusters:
        return AssetsClusters(
            clusters=self.clusters.load(),
        )

    def save(self, data: AssetsClusters) -> None:
        self.clusters.save(data=data.clusters)


@dataclass
class IndicsClustersFiles(FilesObject[IndicsClusters]):
    clusters: JSONFile[str, dict[str, list[str]]]

    def get(self) -> IndicsClusters:
        return IndicsClusters(
            clusters=self.clusters.load(),
        )

    def save(self, data: IndicsClusters) -> None:
        self.clusters.save(data=data.clusters)


@dataclass
class AssetFiles(FilesObject[AssetsConfig]):
    active: JSONFile[str, bool]

    def get(self) -> AssetsConfig:
        return AssetsConfig(
            assets_active=self.active.load(),
        )

    def save(self, data: AssetsConfig) -> None:
        self.active.save(data=data.get_all_entities_dict())


@dataclass
class IndicFiles(FilesObject[IndicsConfig]):
    active: JSONFile[str, bool]
    params: JSONFile[str, dict[str, list[int]]]

    def get(self) -> IndicsConfig:
        return IndicsConfig(
            indics_active=self.active.load(),
            params_config=self.params.load(),
        )

    def save(self, data: IndicsConfig) -> None:
        self.active.save(data=data.get_all_entities_dict())
        self.params.save(data=data.prepare_indic_params())


@dataclass
class TickersData(FilesObject[DataFrameFloat]):
    returns: ParquetFile

    def get(self, assets: list[str] | None) -> DataFrameFloat:
        return DataFrameFloat(self.returns.load(names=assets))

    def save(self, data: DataFrameFloat) -> None:
        self.returns.save(data=data)

    def refresh(self, assets: list[str]) -> None:
        data: DataFrameFloat = fetch_data(assets=assets)
        self.save(data=data)
