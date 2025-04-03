from dataclasses import dataclass

from outquantlab.core.clusters import (
    AssetsClusters,
    AssetsClustersTuples,
    ClustersHierarchy,
    IndicsClusters,
    IndicsClustersTuples,
)
from outquantlab.core.collections import AssetsConfig, IndicsConfig
from outquantlab.indicators import BaseIndic


@dataclass(slots=True)
class BacktestConfig:
    indics_params: list[BaseIndic]
    hierarchy: ClustersHierarchy


@dataclass(slots=True)
class AppConfig:
    indics_config: IndicsConfig
    assets_config: AssetsConfig
    assets_clusters: AssetsClusters
    indics_clusters: IndicsClusters

    def get_backtest_config(
        self,
    ) -> BacktestConfig:
        self.indics_clusters.check_data_structure(
            entities=self.indics_config.get_all_entities()
        )
        indics_params: list[BaseIndic] = self.indics_config.get_indics_params()
        indics_tuples: list[IndicsClustersTuples] = (
            self.indics_clusters.get_clusters_tuples(entities=indics_params)
        )

        self.assets_clusters.check_data_structure(
            entities=self.assets_config.get_all_entities()
        )
        asset_tuples: list[AssetsClustersTuples] = (
            self.assets_clusters.get_clusters_tuples(
                entities=self.assets_config.get_all_active_entities()
            )
        )

        hierarchy = ClustersHierarchy(
            asset_tuples=asset_tuples,
            indics_tuples=indics_tuples,
        )
        return BacktestConfig(
            hierarchy=hierarchy,
            indics_params=indics_params,
        )
