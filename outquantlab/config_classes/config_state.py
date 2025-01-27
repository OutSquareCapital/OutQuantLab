from dataclasses import dataclass, field

from pandas import MultiIndex

from outquantlab.config_classes.clusters import (
    AssetsClusters,
    BaseIndic,
    IndicsClusters,
    generate_levels,
)
from outquantlab.config_classes.collections import AssetsCollection, IndicsCollection
from outquantlab.config_classes.progress_statut import ProgressStatus


@dataclass(slots=True)
class BacktestConfig:
    multi_index: MultiIndex
    indics_params: list[BaseIndic]
    assets_nb: int
    clusters_names: list[str]
    total_returns_streams: int
    clusters_nb: int
    progress: ProgressStatus = field(init=False)

    def __post_init__(self) -> None:
        self.progress = ProgressStatus(
            total_returns_streams=self.total_returns_streams,
            clusters_nb=self.clusters_nb,
        )


@dataclass(slots=True)
class ConfigState:
    indics_collection: IndicsCollection
    assets_collection: AssetsCollection
    assets_clusters: AssetsClusters
    indics_clusters: IndicsClusters

    def get_backtest_config(
        self,
    ) -> BacktestConfig:
        indics_params: list[BaseIndic] = self.indics_collection.get_indics_params()
    
        asset_tuples: list[tuple[str, ...]] = self.assets_clusters.get_clusters_tuples(
            entities=self.assets_collection.get_all_active_entities()
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
        return BacktestConfig(
            multi_index=multi_index,
            indics_params=indics_params,
            assets_nb=len(asset_tuples),
            clusters_names=multi_index.names,
            total_returns_streams=len(multi_index),
            clusters_nb=num_levels - 1,
        )
