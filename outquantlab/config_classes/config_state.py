from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple

from pandas import MultiIndex

from outquantlab.config_classes.clusters import (
    AssetsClusters,
    BaseIndic,
    IndicsClusters,
)
from outquantlab.config_classes.collections import AssetsConfig, IndicsConfig


class ClustersLevels(StrEnum):
    ASSETS_CLUSTERS = "assets_clusters"
    ASSETS_SUBCLUSTERS = "assets_subclusters"
    ASSETS = "assets"
    INDICS_CLUSTERS = "indics_clusters"
    INDICS_SUBCLUSTERS = "indics_subclusters"
    INDICS = "indics"
    PARAMS = "params"


class BacktestConfig(NamedTuple):
    multi_index: MultiIndex
    indics_params: list[BaseIndic]


@dataclass(slots=True)
class AppConfig:
    indics_config: IndicsConfig
    assets_config: AssetsConfig
    assets_clusters: AssetsClusters
    indics_clusters: IndicsClusters

    def get_backtest_config(
        self,
    ) -> BacktestConfig:
        indics_params: list[BaseIndic] = self.indics_config.get_indics_params()

        asset_tuples: list[tuple[str, ...]] = self.assets_clusters.get_clusters_tuples(
            entities=self.assets_config.get_all_active_entities()
        )
        indics_tuples: list[tuple[str, ...]] = self.indics_clusters.get_clusters_tuples(
            entities=indics_params
        )
        return BacktestConfig(
            multi_index=_get_multi_index(
                asset_tuples=asset_tuples,
                indics_tuples=indics_tuples,
            ),
            indics_params=indics_params,
        )


def _get_multi_index(
    asset_tuples: list[tuple[str, ...]],
    indics_tuples: list[tuple[str, ...]],
) -> MultiIndex:
    product_tuples: list[tuple[str, ...]] = [
        (*asset_clusters, *indic_clusters)
        for indic_clusters in indics_tuples
        for asset_clusters in asset_tuples
    ]

    return MultiIndex.from_tuples(  # type: ignore
        tuples=product_tuples,
        names=[name.value for name in ClustersLevels],
    )
