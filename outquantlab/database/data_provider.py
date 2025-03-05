import pandas as pd

import outquantlab.config_classes as cfg
from outquantlab.database.data_file import DataFile
from outquantlab.database.data_queries import DataQueries
from outquantlab.database.data_refresher import get_yf_data
from outquantlab.database.data_structure import FileNames
from outquantlab.typing_conventions import DataFrameFloat


class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def refresh_assets_data(self, assets: list[str]) -> None:
        prices_data, returns_data = get_yf_data(assets=assets)
        self._save_assets_data(prices_data=prices_data, returns_data=returns_data)

    def get_returns_data(self, names: list[str]) -> DataFrameFloat:
        return DataFrameFloat(
            data=self.dbq.select(file_name=FileNames.RETURNS_DATA).load(
                default_value=pd.DataFrame(), names=names
            )
        )

    def get_app_config(self) -> cfg.AppConfig:
        return cfg.AppConfig(
            indics_config=_instanciate_indics_config(
                indics_active_file=self.dbq.select(file_name=FileNames.INDICS_ACTIVE),
                indics_params_file=self.dbq.select(file_name=FileNames.INDICS_PARAMS),
            ),
            assets_config=_instanciate_assets_config(
                assets_active_file=self.dbq.select(file_name=FileNames.ASSETS_ACTIVE),
                assets_names_file=self.dbq.select(file_name=FileNames.ASSETS_NAMES),
            ),
            assets_clusters=_instanciate_assets_clusters_tree(
                file=self.dbq.select(file_name=FileNames.ASSETS_CLUSTERS)
            ),
            indics_clusters=_instanciate_indics_clusters_tree(
                file=self.dbq.select(file_name=FileNames.INDICS_CLUSTERS)
            ),
        )

    def save_app_config(
        self,
        config: cfg.AppConfig,
    ) -> None:
        self.dbq.select(file_name=FileNames.ASSETS_ACTIVE).save(
            data=config.assets_config.get_all_entities_dict()
        )
        self.dbq.select(file_name=FileNames.INDICS_ACTIVE).save(
            data=config.indics_config.get_all_entities_dict()
        )
        self.dbq.select(file_name=FileNames.INDICS_PARAMS).save(
            data=config.indics_config.prepare_indic_params()
        )
        self.dbq.select(file_name=FileNames.ASSETS_CLUSTERS).save(
            data=config.assets_clusters.clusters
        )
        self.dbq.select(file_name=FileNames.INDICS_CLUSTERS).save(
            data=config.indics_clusters.clusters
        )

    def _save_assets_data(
        self, prices_data: DataFrameFloat, returns_data: DataFrameFloat
    ) -> None:
        assets_names: list[str] = prices_data.columns.to_list()

        self.dbq.select(file_name=FileNames.PRICES_DATA.value).save(data=prices_data)
        self.dbq.select(file_name=FileNames.RETURNS_DATA.value).save(data=returns_data)
        self.dbq.select(file_name=FileNames.ASSETS_NAMES.value).save(data=assets_names)


def _instanciate_assets_config(
    assets_active_file: DataFile, assets_names_file: DataFile
) -> cfg.AssetsConfig:
    return cfg.AssetsConfig(
        assets_active=assets_active_file.load(default_value={}),
        asset_names=assets_names_file.load(default_value=[]),
    )


def _instanciate_indics_config(
    indics_active_file: DataFile, indics_params_file: DataFile
) -> cfg.IndicsConfig:
    return cfg.IndicsConfig(
        indics_active=indics_active_file.load(default_value={}),
        params_config=indics_params_file.load(default_value={}),
    )


def _instanciate_assets_clusters_tree(file: DataFile) -> cfg.AssetsClusters:
    return cfg.AssetsClusters(clusters=file.load(default_value={}))


def _instanciate_indics_clusters_tree(file: DataFile) -> cfg.IndicsClusters:
    return cfg.IndicsClusters(clusters=file.load(default_value={}))
