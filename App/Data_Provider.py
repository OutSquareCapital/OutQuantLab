from config_classes import (
    AssetsCollection,
    ClustersTree,
    IndicatorsCollection,
)
from database import DataQueries
from typing_conventions import ArrayFloat, DataFrameFloat

class DataBaseProvider:
    def __init__(self) -> None:
        self.dbq = DataQueries()

    def get_assets_returns(self, asset_names: list[str]) -> ArrayFloat:
        returns_df = DataFrameFloat(
            data=self.dbq.select(file="returns_data").load(names=asset_names)
        )
        return returns_df.nparray

    def get_initial_data(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=self.dbq.select(file="returns_data").load(names=["Date", "SPY"])
        )

    def get_assets_collection(self) -> AssetsCollection:
        return AssetsCollection(
            assets_to_test=self.dbq.select(file="assets_to_test").load(),
            asset_names=self.dbq.select(file="assets_names").load(),
        )

    def get_indicators_collection(self) -> IndicatorsCollection:
        return IndicatorsCollection(
            indicators_to_test=self.dbq.select(file="indics_to_test").load(),
            params_config=self.dbq.select(file="indics_params").load(),
        )

    def get_clusters_tree(self, cluster_type: str) -> ClustersTree:
        prefix = "Asset" if cluster_type == "assets" else "Indic"
        return ClustersTree(
            clusters=self.dbq.select(file=f"{cluster_type}_clusters").load(),
            prefix=prefix,
        )

    def save_assets_collection(self, assets_collection: AssetsCollection) -> None:
        self.dbq.select(file="assets_to_test").save(
            data=assets_collection.all_active_entities_dict
        )

    def save_indicators_collection(
        self, indics_collection: IndicatorsCollection
    ) -> None:
        self.dbq.select(file="indics_to_test").save(
            data=indics_collection.all_active_entities_dict
        )
        self.dbq.select(file="indics_params").save(
            data={
            name: indicator.params_values for name, indicator in indics_collection.entities.items()
        }
        )

    def save_clusters_tree(
        self, clusters_tree: ClustersTree, cluster_type: str
    ) -> None:
        self.dbq.select(file=f"{cluster_type}_clusters").save(
            data=clusters_tree.clusters
        )
