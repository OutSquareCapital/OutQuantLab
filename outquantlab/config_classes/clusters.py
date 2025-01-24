from typing import Any

import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore
from scipy.spatial.distance import squareform

from outquantlab.config_classes.collections import BaseIndicator
from outquantlab.metrics import calculate_distance_matrix
from outquantlab.typing_conventions import ArrayFloat, ClustersHierarchy, DataFrameFloat


class ClustersTree:
    def __init__(self, clusters: ClustersHierarchy, prefix: str) -> None:
        self.clusters: ClustersHierarchy = clusters
        self.prefix: str = prefix
        self.clusters_structure: list[str] = []
        self._generate_clusters_structure()

    def _generate_clusters_structure(self) -> None:
        def determine_depth(node: dict[str, Any] | list[str]) -> int:
            if isinstance(node, dict):
                return 1 + max(
                    determine_depth(node=subnode) for subnode in node.values()
                )
            return 0

        depth: int = determine_depth(self.clusters)
        for i in range(depth):
            cluster_name: str = f"{self.prefix}{'Sub' * i}Cluster"
            self.clusters_structure.append(cluster_name)
        self.clusters_structure.append(self.prefix)

    def update_clusters_structure(self, new_structure: ClustersHierarchy) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            entity: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, entities in subclusters.items()
            for entity in entities
        }


def generate_multi_index_process(
    indic_clusters_structure: list[str],
    asset_clusters_structure: list[str],
    indics_params: list[BaseIndicator],
    assets: list[str],
    assets_to_clusters: dict[str, tuple[str, ...]],
    indics_to_clusters: dict[str, tuple[str, ...]],
) -> pd.MultiIndex:
    asset_tuples: list[tuple[*tuple[str, ...], str]] = [
        (*assets_to_clusters[asset], asset) for asset in assets
    ]

    indic_param_tuples: list[tuple[*tuple[str, ...], str, str]] = [
        (*indics_to_clusters[indic.name], indic.name, "_".join(map(str, combo)))
        for indic in indics_params
        for combo in indic.param_combos
    ]

    product_tuples: list[tuple[str, ...]] = [
        (*asset_clusters, *indic_clusters)
        for indic_clusters in indic_param_tuples
        for asset_clusters in asset_tuples
    ]

    
    return pd.MultiIndex.from_tuples(  # type: ignore
        tuples=product_tuples,
        names=asset_clusters_structure + indic_clusters_structure + ["Param"],
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
