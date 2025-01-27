from outquantlab.config_classes.collections import IndicsCollection, AssetsCollection
from outquantlab.config_classes.clusters import (
    AssetsClusters,
    IndicsClusters,
    Asset,
    BaseIndic,
    generate_levels,
)
from dataclasses import dataclass
from outquantlab.config_classes.progress_statut import ProgressStatus
from pandas import MultiIndex


@dataclass(slots=True)
class ClustersIndex:
    multi_index: MultiIndex
    assets_nb: int
    clusters_names: list[str]
    total_returns_streams: int
    clusters_nb: int

    def get_progress(self) -> ProgressStatus:
        return ProgressStatus(
            total_returns_streams=self.total_returns_streams,
            clusters_nb=self.clusters_nb,
        )

@dataclass()
class ConfigState:
    indics_collection: IndicsCollection
    assets_collection: AssetsCollection
    assets_clusters: AssetsClusters
    indics_clusters: IndicsClusters

    def generate_multi_index_process(
        self,
        indics_params: list[BaseIndic],
        assets: list[Asset],
    ) -> ClustersIndex:
        asset_tuples: list[tuple[str, ...]] = self.assets_clusters.get_clusters_tuples(
            entities=assets
        )
        indics_tuples: list[tuple[str, ...]] = self.indics_clusters.get_clusters_tuples(
            entities=indics_params
        )
        product_tuples: list[tuple[str, ...]] = [
            (*asset_clusters, *indic_clusters)
            for indic_clusters in indics_tuples
            for asset_clusters in asset_tuples
        ]
        num_levels: int = len(product_tuples[0])
        multi_index: MultiIndex = MultiIndex.from_tuples(  # type: ignore
            tuples=product_tuples,
            names=generate_levels(num_levels=num_levels),
        )
        return ClustersIndex(
            multi_index=multi_index,
            assets_nb=len(asset_tuples),
            clusters_names=multi_index.names,
            total_returns_streams=len(multi_index),
            clusters_nb=num_levels - 1,
        )
