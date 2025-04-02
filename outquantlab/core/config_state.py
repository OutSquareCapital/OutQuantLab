from dataclasses import dataclass, field

from pandas import MultiIndex

from outquantlab.core.clusters import AssetsClusters, IndicsClusters
from outquantlab.core.collections import AssetsConfig, IndicsConfig
from outquantlab.indicators import BaseIndic
from outquantlab.metrics import get_overall_mean
from outquantlab.structures import DataFrameFloat


@dataclass
class BacktestResults:
    assets_clusters: DataFrameFloat = field(default_factory=DataFrameFloat)
    assets_subclusters: DataFrameFloat = field(default_factory=DataFrameFloat)
    assets: DataFrameFloat = field(default_factory=DataFrameFloat)
    indics_clusters: DataFrameFloat = field(default_factory=DataFrameFloat)
    indics_subclusters: DataFrameFloat = field(default_factory=DataFrameFloat)
    indics: DataFrameFloat = field(default_factory=DataFrameFloat)
    params: DataFrameFloat = field(default_factory=DataFrameFloat)

    @property
    def clusters_levels(self) -> list[str]:
        return [name for name in self.__dict__.keys()]

    @property
    def clusters_depth(self) -> int:
        return len(self.__dict__.keys())

    @property
    def portfolio(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=get_overall_mean(array=self.assets_clusters.get_array(), axis=1),
            index=self.assets_clusters.dates,
            columns=["portfolio"],
        )

    def __getitem__(self, key: str) -> DataFrameFloat:
        value: DataFrameFloat = self.__dict__[key]
        return value

    def __setitem__(self, key: str, value: DataFrameFloat) -> None:
        self.__dict__[key] = value


@dataclass(slots=True)
class BacktestConfig:
    indics_params: list[BaseIndic]
    multi_index: MultiIndex
    backtest_results: BacktestResults


def _get_multi_index(
    clusters_levels: list[str],
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
        names=[name for name in clusters_levels],
    )


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
        indics_tuples: list[tuple[str, ...]] = self.indics_clusters.get_clusters_tuples(
            entities=indics_params
        )
        self.assets_clusters.check_data_structure(
            entities=self.assets_config.get_all_entities()
        )
        asset_tuples: list[tuple[str, ...]] = self.assets_clusters.get_clusters_tuples(
            entities=self.assets_config.get_all_active_entities()
        )

        backtest_results: BacktestResults = BacktestResults()
        return BacktestConfig(
            backtest_results=backtest_results,
            multi_index=_get_multi_index(
                asset_tuples=asset_tuples,
                indics_tuples=indics_tuples,
                clusters_levels=backtest_results.clusters_levels,
            ),
            indics_params=indics_params,
        )
