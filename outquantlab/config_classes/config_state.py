from dataclasses import dataclass, field
from outquantlab.config_classes.clusters import AssetsClusters, IndicsClusters
from outquantlab.config_classes.collections import AssetsConfig, IndicsConfig
from outquantlab.typing_conventions import DataFrameFloat
from pandas import MultiIndex
from outquantlab.indicators import BaseIndic
from outquantlab.metrics import get_overall_mean


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
        return self.__dict__[key]

    def __setitem__(self, key: str, value: DataFrameFloat) -> None:
        self.__dict__[key] = value

    def aggregate_raw_returns(self, returns_df: DataFrameFloat) -> None:
        for lvl in range(self.clusters_depth, 0, -1):
            returns_df = self._get_portfolio_returns(
                returns_df=returns_df,
                grouping_levels=returns_df.columns.names[:lvl],
            )

            returns_df.dropna(axis=0, how="any", inplace=True)  # type: ignore
            key_name: str = returns_df.columns.names[lvl - 1]
            self[key_name] = returns_df

    def _get_portfolio_returns(
        self, returns_df: DataFrameFloat, grouping_levels: list[str]
    ) -> DataFrameFloat:
        return DataFrameFloat(
            data=returns_df.T.groupby(  # type: ignore
                level=grouping_levels, observed=True
            )
            .mean()
            .T
        )


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
        indics_params: list[BaseIndic] = self.indics_config.get_indics_params()

        asset_tuples: list[tuple[str, ...]] = self.assets_clusters.get_clusters_tuples(
            entities=self.assets_config.get_all_active_entities()
        )
        indics_tuples: list[tuple[str, ...]] = self.indics_clusters.get_clusters_tuples(
            entities=indics_params
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
