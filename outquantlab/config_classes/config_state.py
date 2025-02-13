from dataclasses import dataclass, field

from pandas import MultiIndex

from outquantlab.config_classes.clusters import (
    AssetsClusters,
    BaseIndic,
    IndicsClusters,
    generate_levels,
)
from outquantlab.config_classes.collections import AssetsConfig, IndicsConfig
from outquantlab.typing_conventions import ArrayFloat, Float32
from numpy import empty


@dataclass(slots=True)
class BacktestData:
    assets_nb: int
    start_index: int = 0
    data: ArrayFloat = field(default_factory=lambda: empty(shape=(0, 0), dtype=Float32))

    def get_data_array(self, nb_days: int, total_returns_streams: int) -> None:
        self.data = empty(
            shape=(nb_days, total_returns_streams),
            dtype=Float32,
        )

    def fill_data_array(
        self,
        results: list[ArrayFloat],
        strategies_nb: int,
    ) -> None:
        for i in range(strategies_nb):
            end_index: int = self.start_index + self.assets_nb
            self.data[:, self.start_index : end_index] = results[i]
            self.start_index = end_index


@dataclass(slots=True, frozen=True)
class BacktestConfig:
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
            names=generate_levels(num_levels=num_levels),
        )
        return BacktestConfig(
            multi_index=multi_index,
            indics_params=indics_params
        )
