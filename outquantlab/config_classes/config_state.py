from dataclasses import dataclass

from pandas import MultiIndex

from outquantlab.config_classes.clusters import (
    AssetsClusters,
    BaseIndic,
    IndicsClusters,
    generate_levels,
)
from outquantlab.config_classes.collections import AssetsConfig, IndicsConfig
from outquantlab.config_classes.progress_statut import ProgressStatus


@dataclass(slots=True)
class BacktestConfig:
    multi_index: MultiIndex
    indics_params: list[BaseIndic]
    clusters_names: list[str]
    clusters_nb: int
    assets_nb: int
    total_returns_streams: int
    progress = ProgressStatus()


@dataclass(slots=True)
class AppConfig:
    indics_config: IndicsConfig
    assets_config: AssetsConfig
    assets_clusters: AssetsClusters
    indics_clusters: IndicsClusters


def get_backtest_config(
    app_config: AppConfig,
) -> BacktestConfig:
    indics_params: list[BaseIndic] = app_config.indics_config.get_indics_params()

    asset_tuples: list[tuple[str, ...]] = (
        app_config.assets_clusters.get_clusters_tuples(
            entities=app_config.assets_config.get_all_active_entities()
        )
    )
    indics_tuples: list[tuple[str, ...]] = (
        app_config.indics_clusters.get_clusters_tuples(entities=indics_params)
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
        clusters_nb=num_levels - 1,
        total_returns_streams=len(multi_index),
    )
