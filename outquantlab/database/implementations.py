from dataclasses import dataclass

from outquantlab.config_classes import (
    AssetsClusters,
    AssetsConfig,
    IndicsClusters,
    IndicsConfig,
)
from outquantlab.database.interfaces import FilesObject, JSONFile, ParquetFile
from outquantlab.web_api import AssetsData, fetch_data
from outquantlab.typing_conventions import DataFrameFloat

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
class TickersData(FilesObject[AssetsData]):
    returns: ParquetFile
    prices: ParquetFile

    def get(self, assets: list[str]) -> AssetsData:
        return fetch_data(assets=assets)

    def save(self, data: AssetsData) -> None:
        self.prices.save(data=data.prices)
        self.returns.save(data=data.returns)

    def refresh(self, assets: list[str]) -> None:
        data: AssetsData = self.get(assets=assets)
        self.save(data=data)

    def get_returns_data(self, assets: list[str]) -> DataFrameFloat:
        data: AssetsData = self.get(assets=assets)
        return data.returns