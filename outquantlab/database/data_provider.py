import outquantlab.config_classes as cfg
from outquantlab.database.data_queries import DataQueries
from outquantlab.database.data_structure import FileNames
from outquantlab.typing_conventions import DataFrameFloat


class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def get_data(self, names: list[str]) -> DataFrameFloat:
        return DataFrameFloat(
            data=self.dbq.select(file=FileNames.RETURNS_DATA.value).load(names=names)
        )

    def get_config(self) -> cfg.AppConfig:
        return cfg.AppConfig(
            indics_config=_get_indics_config(dbq=self.dbq),
            assets_config=_get_assets_config(dbq=self.dbq),
            assets_clusters=_get_assets_clusters_tree(dbq=self.dbq),
            indics_clusters=_get_indics_clusters_tree(dbq=self.dbq),
        )

    def save_config(
        self,
        config: cfg.AppConfig,
    ) -> None:
        _save_assets_config(
            dbq=self.dbq, assets=config.assets_config.get_all_entities_dict()
        )
        _save_indics_config(
            dbq=self.dbq, indics=config.indics_config.get_all_entities_dict()
        )
        _save_indics_data(
            dbq=self.dbq, indics_data=config.indics_config.prepare_indic_params()
        )
        _save_assets_clusters_tree(
            dbq=self.dbq, clusters=config.assets_clusters.clusters
        )
        _save_indics_clusters_tree(
            dbq=self.dbq, clusters=config.indics_clusters.clusters
        )


def _get_assets_config(dbq: DataQueries) -> cfg.AssetsConfig:
    return cfg.AssetsConfig(
        assets_to_test=_get_assets_to_test(
            dbq=dbq, file_name=FileNames.ASSETS_TO_TEST.value
        ),
        asset_names=_get_asset_names(dbq=dbq, file_name=FileNames.ASSETS_NAMES.value),
    )


def _get_indics_config(dbq: DataQueries) -> cfg.IndicsConfig:
    return cfg.IndicsConfig(
        indics_to_test=_get_indics_to_test(
            dbq=dbq, file_name=FileNames.INDICS_TO_TEST.value
        ),
        params_config=_get_indics_params(
            dbq=dbq, file_name=FileNames.INDICS_PARAMS.value
        ),
    )


def _get_assets_clusters_tree(dbq: DataQueries) -> cfg.AssetsClusters:
    return cfg.AssetsClusters(
        clusters=_get_clusters(dbq=dbq, file_name=FileNames.ASSETS_CLUSTERS.value)
    )


def _get_indics_clusters_tree(dbq: DataQueries) -> cfg.IndicsClusters:
    return cfg.IndicsClusters(
        clusters=_get_clusters(dbq=dbq, file_name=FileNames.INDICS_CLUSTERS.value)
    )


def _save_assets_config(dbq: DataQueries, assets: dict[str, bool]) -> None:
    dbq.select(file=FileNames.ASSETS_TO_TEST.value).save(data=assets)


def _save_indics_config(dbq: DataQueries, indics: dict[str, bool]) -> None:
    dbq.select(file=FileNames.INDICS_TO_TEST.value).save(data=indics)


def _save_indics_data(
    dbq: DataQueries, indics_data: dict[str, dict[str, list[int]]]
) -> None:
    dbq.select(file=FileNames.INDICS_PARAMS.value).save(data=indics_data)


def _save_assets_clusters_tree(
    dbq: DataQueries, clusters: dict[str, dict[str, list[str]]]
) -> None:
    dbq.select(file=FileNames.ASSETS_CLUSTERS.value).save(data=clusters)


def _save_indics_clusters_tree(
    dbq: DataQueries, clusters: dict[str, dict[str, list[str]]]
) -> None:
    dbq.select(file=FileNames.INDICS_CLUSTERS.value).save(data=clusters)


def _get_assets_to_test(dbq: DataQueries, file_name: str) -> dict[str, bool]:
    try:
        assets_to_test: dict[str, bool] = dbq.select(file=file_name).load()
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        assets_to_test = {}
    return assets_to_test


def _get_asset_names(dbq: DataQueries, file_name: str) -> list[str]:
    try:
        asset_names: list[str] = dbq.select(file=file_name).load()
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        asset_names = []
    return asset_names


def _get_indics_to_test(dbq: DataQueries, file_name: str) -> dict[str, bool]:
    try:
        indics_to_test: dict[str, bool] = dbq.select(file=file_name).load()
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        indics_to_test = {}
    return indics_to_test


def _get_indics_params(
    dbq: DataQueries, file_name: str
) -> dict[str, dict[str, list[int]]]:
    try:
        params_config: dict[str, dict[str, list[int]]] = dbq.select(
            file=file_name
        ).load()
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        params_config = {}
    return params_config


def _get_clusters(dbq: DataQueries, file_name: str) -> dict[str, dict[str, list[str]]]:
    try:
        clusters: dict[str, dict[str, list[str]]] = dbq.select(file=file_name).load()
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        clusters = {}
    return clusters
