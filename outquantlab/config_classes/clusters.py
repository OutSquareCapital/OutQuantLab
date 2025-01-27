from pandas import MultiIndex
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.config_classes.collections import Asset
from outquantlab.indicators import BaseIndic
from outquantlab.config_classes.generic_classes import BaseClustersTree
from outquantlab.metrics import calculate_distance_matrix
from outquantlab.typing_conventions import ArrayFloat, ClustersHierarchy, DataFrameFloat
from dataclasses import dataclass
from outquantlab.config_classes.progress_statut import ProgressStatus


@dataclass(slots=True)
class ClustersIndex:
    multi_index: MultiIndex
    total_returns_streams: int = 0
    clusters_nb: int = 0
    clusters_names: list[str] = []

    def __post_init__(self) -> None:
        self.clusters_names: list[str] = self.multi_index.names
        self.total_returns_streams: int = len(self.multi_index)
        self.clusters_nb: int = len(self.multi_index.names) - 1

    def get_progress(self) -> ProgressStatus:
        return ProgressStatus(
            total_returns_streams=self.total_returns_streams,
            clusters_nb=self.clusters_nb,
        )


class AssetsClusters(BaseClustersTree):
    def __init__(self, clusters: ClustersHierarchy) -> None:
        super().__init__(clusters=clusters, prefix="Asset")

    def get_clusters_tuples(self, entities: list[Asset]) -> list[tuple[str, ...]]:
        assets_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [(*assets_to_clusters[asset.name], asset.name) for asset in entities]


class IndicsClusters(BaseClustersTree):
    def __init__(self, clusters: ClustersHierarchy) -> None:
        super().__init__(clusters=clusters, prefix="Indic")

    def get_clusters_tuples(self, entities: list[BaseIndic]) -> list[tuple[str, ...]]:
        indics_to_clusters: dict[str, tuple[str, ...]] = (
            self.map_nested_clusters_to_entities()
        )
        return [
            (*indics_to_clusters[indic.name], indic.name, "_".join(map(str, combo)))
            for indic in entities
            for combo in indic.param_combos
        ]


def generate_levels(product_tuples: list[tuple[str, ...]]) -> list[str]:
    num_levels: int = len(product_tuples[0])
    return [f"lvl{i + 1}" for i in range(num_levels)]


def generate_multi_index_process(
    indic_param_tuples: list[tuple[str, ...]],
    asset_tuples: list[tuple[str, ...]],
) -> ClustersIndex:
    product_tuples: list[tuple[str, ...]] = [
        (*asset_clusters, *indic_clusters)
        for indic_clusters in indic_param_tuples
        for asset_clusters in asset_tuples
    ]

    multi_index: MultiIndex = MultiIndex.from_tuples(  # type: ignore
        tuples=product_tuples,
        names=generate_levels(product_tuples=product_tuples),
    )

    return ClustersIndex(
        multi_index=multi_index
    )


def get_flat_clusters(returns_array: ArrayFloat, max_clusters: int) -> list[int]:
    distance_matrix: ArrayFloat = calculate_distance_matrix(returns_array=returns_array)
    distance_condensed: ArrayFloat = squareform(distance_matrix, checks=False)
    linkage_matrix: ArrayFloat = linkage(distance_condensed, method="ward")
    return fcluster(linkage_matrix, max_clusters, criterion="maxclust")


def get_assets_in_cluster(
    cluster_id: int, asset_names: list[str], flat_clusters: list[int]
) -> list[str]:
    return [
        asset
        for asset, cluster in zip(asset_names, flat_clusters)
        if cluster == cluster_id
    ]


def assign_clusters(
    max_clusters: int, asset_names: list[str], flat_clusters: list[int]
) -> dict[str, list[str]]:
    return {
        str(object=cluster_id): get_assets_in_cluster(
            cluster_id=cluster_id, asset_names=asset_names, flat_clusters=flat_clusters
        )
        for cluster_id in range(1, max_clusters + 1)
    }


def generate_dynamic_clusters(
    returns_df: DataFrameFloat, max_clusters: int
) -> dict[str, list[str]]:
    flat_clusters: list[int] = get_flat_clusters(
        returns_array=returns_df.get_array(), max_clusters=max_clusters
    )
    asset_names: list[str] = returns_df.columns.tolist()

    return assign_clusters(
        max_clusters=max_clusters, asset_names=asset_names, flat_clusters=flat_clusters
    )
