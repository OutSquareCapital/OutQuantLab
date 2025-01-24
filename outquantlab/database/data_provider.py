from outquantlab.config_classes import (
    AssetsClusters,
    AssetsCollection,
    IndicsClusters,
    IndicsCollection,
)
from outquantlab.database.data_queries import DataQueries
from outquantlab.indicators import DataArrays
from outquantlab.typing_conventions import DataFrameFloat


class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def get_initial_data(self) -> DataFrameFloat:
        return DataFrameFloat(data=self.dbq.select(file="returns_data").load())

    def get_assets_collection(self) -> AssetsCollection:
        return AssetsCollection(
            assets_to_test=self.dbq.select(file="assets_to_test").load(),
            asset_names=self.dbq.select(file="assets_names").load(),
        )

    def get_indics_collection(self, data_arrays: DataArrays) -> IndicsCollection:
        return IndicsCollection(
            indics_to_test=self.dbq.select(file="indics_to_test").load(),
            params_config=self.dbq.select(file="indics_params").load(),
            data_arrays=data_arrays,
        )

    def get_assets_clusters_tree(self) -> AssetsClusters:
        return AssetsClusters(
            clusters=self.dbq.select(file="assets_clusters").load(),
        )

    def get_indics_clusters_tree(self) -> IndicsClusters:
        return IndicsClusters(
            clusters=self.dbq.select(file="indics_clusters").load(),
        )

    def save_assets_collection(self, assets_collection: AssetsCollection) -> None:
        self.dbq.select(file="assets_to_test").save(
            data=assets_collection.get_all_entities_dict()
        )

    def save_indics_collection(self, indics_collection: IndicsCollection) -> None:
        self.dbq.select(file="indics_to_test").save(
            data=indics_collection.get_all_entities_dict()
        )
        self.dbq.select(file="indics_params").save(
            data={
                name: indicator.params_values
                for name, indicator in indics_collection.entities.items()
            }
        )

    def save_assets_clusters_tree(self, clusters_tree: AssetsClusters) -> None:
        self.dbq.select(file="assets_clusters").save(data=clusters_tree.clusters)

    def save_indics_clusters_tree(self, clusters_tree: IndicsClusters) -> None:
        self.dbq.select(file="indics_clusters").save(data=clusters_tree.clusters)
