from outquantlab.config_classes import (
    AssetsClusters,
    AssetsConfig,
    IndicsClusters,
    IndicsConfig,
    AppConfig,
)
from outquantlab.database.data_queries import DataQueries
from outquantlab.typing_conventions import DataFrameFloat

class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def get_data(self, names: list[str]) -> DataFrameFloat:
    
        return DataFrameFloat(
            data=self.dbq.select(file="returns_data").load(names=names)
        )

    def get_config(self) -> AppConfig:
        return AppConfig(
            indics_config=self._get_indics_config(),
            assets_config=self._get_assets_config(),
            assets_clusters=self._get_assets_clusters_tree(),
            indics_clusters=self._get_indics_clusters_tree(),
        )

    def save_config(
        self,
        config: AppConfig,
    ) -> None:
        self._save_assets_config(assets_collection=config.assets_config)
        self._save_indics_config(indics_collection=config.indics_config)
        self._save_assets_clusters_tree(clusters_tree=config.assets_clusters)
        self._save_indics_clusters_tree(clusters_tree=config.indics_clusters)

    def _get_assets_config(self) -> AssetsConfig:
        return AssetsConfig(
            assets_to_test=self.dbq.select(file="assets_to_test").load(),
            asset_names=self.dbq.select(file="assets_names").load(),
        )

    def _get_indics_config(self) -> IndicsConfig:
        return IndicsConfig(
            indics_to_test=self.dbq.select(file="indics_to_test").load(),
            params_config=self.dbq.select(file="indics_params").load(),
        )

    def _get_assets_clusters_tree(self) -> AssetsClusters:
        return AssetsClusters(
            clusters=self.dbq.select(file="assets_clusters").load(),
        )

    def _get_indics_clusters_tree(self) -> IndicsClusters:
        return IndicsClusters(
            clusters=self.dbq.select(file="indics_clusters").load(),
        )

    def _save_assets_config(self, assets_collection: AssetsConfig) -> None:
        self.dbq.select(file="assets_to_test").save(
            data=assets_collection.get_all_entities_dict()
        )

    def _save_indics_config(self, indics_collection: IndicsConfig) -> None:
        self.dbq.select(file="indics_to_test").save(
            data=indics_collection.get_all_entities_dict()
        )
        self.dbq.select(file="indics_params").save(
            data={
                name: indicator.params_values
                for name, indicator in indics_collection.entities.items()
            }
        )

    def _save_assets_clusters_tree(self, clusters_tree: AssetsClusters) -> None:
        self.dbq.select(file="assets_clusters").save(data=clusters_tree.clusters)

    def _save_indics_clusters_tree(self, clusters_tree: IndicsClusters) -> None:
        self.dbq.select(file="indics_clusters").save(data=clusters_tree.clusters)
