from scipy.cluster.hierarchy import linkage, fcluster # type: ignore
from scipy.spatial.distance import squareform
from Utilitary import ArrayFloat, DataFrameFloat, ClustersHierarchy
import pandas as pd
from ConfigClasses.Indicators import Indicator
from Metrics import calculate_distance_matrix

class ClustersTree:
    def __init__(self, clusters: ClustersHierarchy) -> None:
        self.clusters: ClustersHierarchy = clusters

    def update_clusters_structure(self, new_structure: ClustersHierarchy) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            asset: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, assets in subclusters.items()
            for asset in assets
        }

def generate_multi_index_process(
    indicators_params: list[Indicator], 
    asset_names: list[str], 
    assets_clusters: ClustersTree, 
    indics_clusters: ClustersTree
    ) -> tuple[pd.MultiIndex, list[str]]:

    asset_to_clusters: dict[str, tuple[str, str]] = assets_clusters.map_nested_clusters_to_entities()

    indic_to_clusters: dict[str, tuple[str, str]] = indics_clusters.map_nested_clusters_to_entities()

    multi_index_tuples: list[tuple[str, str, str, str, str, str, str]] = []
    clusters_structure: list[str] = ["AssetCluster", "AssetSubCluster", "Asset", "IndicCluster", "IndicSubCluster", "Indicator", "Param"]
    for indic in indicators_params:
        for param in indic.param_combos:
            param_str: str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                asset_cluster1, asset_cluster2 = asset_to_clusters[asset]
                indic_cluster1, indic_cluster2 = indic_to_clusters[indic.name]
                multi_index_tuples.append((
                    asset_cluster1, asset_cluster2, asset, 
                    indic_cluster1, indic_cluster2, 
                    indic.name, param_str
                ))
    multi_index: pd.MultiIndex = pd.MultiIndex.from_tuples( # type: ignore
        tuples=multi_index_tuples, 
        names=clusters_structure)
    return multi_index, clusters_structure

def get_flat_clusters(returns_array: ArrayFloat, max_clusters: int) -> list[int]:
    distance_matrix: ArrayFloat = calculate_distance_matrix(returns_array=returns_array)
    distance_condensed: ArrayFloat = squareform(distance_matrix, checks=False)
    linkage_matrix: ArrayFloat = linkage(distance_condensed, method='ward')
    return fcluster(linkage_matrix, max_clusters, criterion='maxclust')


def generate_dynamic_clusters(
    returns_df: DataFrameFloat, 
    max_clusters: int
) -> dict[str, list[str]]:

    flat_clusters: list[int] = get_flat_clusters(returns_array=returns_df.nparray, max_clusters=max_clusters)
    clusters: dict[str, list[str]] = {}
    asset_names: list[str] = returns_df.columns.tolist()

    for cluster_id in range(1, max_clusters + 1):
        clusters[str(cluster_id)] = [
            asset for asset, cluster in zip(asset_names, flat_clusters) if cluster == cluster_id
        ]
    return clusters