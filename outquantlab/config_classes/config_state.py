from dataclasses import dataclass

from pandas import MultiIndex

from outquantlab.config_classes.clusters import (
    AssetsClusters,
    BaseIndic,
    IndicsClusters,
)
from outquantlab.config_classes.collections import AssetsConfig, IndicsConfig
from typing import NamedTuple

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
        product_tuples: list[tuple[str, ...]] = [
            (*asset_clusters, *indic_clusters)
            for indic_clusters in indics_tuples
            for asset_clusters in asset_tuples
        ]
        num_levels: int = len(product_tuples[0])
        multi_index: MultiIndex = MultiIndex.from_tuples(  # type: ignore
            tuples=product_tuples,
            names=_generate_levels(num_levels=num_levels),
        )
        return BacktestConfig(
            multi_index=multi_index,
            indics_params=indics_params
        )

def _generate_levels(num_levels: int) -> list[str]:
    return [f"lvl{i + 1}" for i in range(num_levels)]