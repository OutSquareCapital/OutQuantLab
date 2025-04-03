from typing import NamedTuple

from pandas import MultiIndex

from outquantlab.core.collections import Asset
from outquantlab.core.interfaces import BaseClustersTree
from outquantlab.indicators import BaseIndic
from outquantlab.metrics import get_overall_mean
from outquantlab.structures import frames


class AssetsClustersTuples(NamedTuple):
    cluster: str
    subcluster: str
    asset: str


class IndicsClustersTuples(NamedTuple):
    cluster: str
    subcluster: str
    indics: str
    params: str


class PortfolioClustersTuples(NamedTuple):
    assets_clusters: str
    assets_subclusters: str
    assets: str
    indics_clusters: str
    indics_subclusters: str
    indics: str
    params: str

CLUSTERS_LEVELS: list[str] = [
    "assets_clusters",
    "assets_subclusters",
    "assets",
    "indics_clusters",
    "indics_subclusters",
    "indics",
    "params",
]


class BacktestResults:
    assets_clusters: frames.DatedFloat
    assets_subclusters: frames.DatedFloat
    assets: frames.DatedFloat
    indics_clusters: frames.DatedFloat
    indics_subclusters: frames.DatedFloat
    indics: frames.DatedFloat
    params: frames.DatedFloat

    def __getitem__(self, key: str) -> frames.DatedFloat:
        value: frames.DatedFloat = self.__dict__[key]
        return value

    def __setitem__(self, key: str, value: frames.DatedFloat) -> None:
        self.__dict__[key] = value

    @property
    def portfolio(self) -> frames.DatedFloat:
        return get_overall_portfolio(data=self.assets_clusters)


class AssetsClusters(BaseClustersTree[Asset, AssetsClustersTuples]):
    def get_clusters_tuples(self, entities: list[Asset]) -> list[AssetsClustersTuples]:
        return [
            AssetsClustersTuples(*self.mapping[asset.name], asset.name)
            for asset in entities
        ]


class IndicsClusters(BaseClustersTree[BaseIndic, IndicsClustersTuples]):
    def get_clusters_tuples(
        self, entities: list[BaseIndic]
    ) -> list[IndicsClustersTuples]:
        return [
            IndicsClustersTuples(
                *self.mapping[indic.name], indic.name, "_".join(map(str, combo))
            )
            for indic in entities
            for combo in indic.params.combos
        ]


class ClustersHierarchy:
    def __init__(
        self,
        asset_tuples: list[AssetsClustersTuples],
        indics_tuples: list[IndicsClustersTuples],
    ) -> None:
        self.product_tuples: list[PortfolioClustersTuples] = [
            PortfolioClustersTuples(
                *asset_tuple,
                *indics_tuple,
            )
            for indics_tuple in indics_tuples
            for asset_tuple in asset_tuples
        ]
    def get_multi_index(self) -> MultiIndex:
        return MultiIndex.from_tuples(  # type: ignore
            tuples=self.product_tuples,
            names=CLUSTERS_LEVELS,
        )
    
    @property
    def length(self) -> int:
        return len(self.product_tuples)

def aggregate_raw_returns(returns_df: frames.DatedFloat) -> BacktestResults:
    results = BacktestResults()
    for lvl in range(len(CLUSTERS_LEVELS), 0, -1):
        returns_df = get_portfolio_returns(
            returns_df=returns_df, grouping_levels=returns_df.columns.names[:lvl]
        )
        returns_df.clean_nans()
        key_name: str = returns_df.columns.names[lvl - 1]
        results[key_name] = returns_df
    return results


def get_portfolio_returns(
    returns_df: frames.DatedFloat, grouping_levels: list[str]
) -> frames.DatedFloat:
    return frames.DatedFloat.from_pandas(
        data=returns_df.T.groupby(level=grouping_levels, observed=True).mean().T  # type: ignore
    )


def get_overall_portfolio(data: frames.DatedFloat) -> frames.DatedFloat:
    return frames.DatedFloat(
        data=get_overall_mean(array=data.get_array(), axis=1),
        index=data.get_index(),
        columns=["portfolio"],
    )
