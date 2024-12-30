from scipy.cluster.hierarchy import linkage, fcluster # type: ignore
from scipy.spatial.distance import squareform
from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth
import pandas as pd
from ConfigClasses.Indicators import Indicator
from typing import TypeAlias
from Metrics import calculate_distance_matrix, calculate_pairwise_distances

ClustersDict: TypeAlias = dict[str, dict[str, list[str]]]

class ClustersTree:
    def __init__(self, clusters: ClustersDict) -> None:
        self.clusters: ClustersDict = clusters

    def update_clusters_structure(self, new_structure: ClustersDict) -> None:
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
    ) -> pd.MultiIndex:

    asset_to_clusters = assets_clusters.map_nested_clusters_to_entities()

    indic_to_clusters = indics_clusters.map_nested_clusters_to_entities()

    multi_index_tuples: list[tuple[str, str, str, str, str, str, str]] = []

    for indic in indicators_params:
        for param in indic.param_combos:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                asset_cluster1, asset_cluster2 = asset_to_clusters[asset]
                indic_cluster1, indic_cluster2 = indic_to_clusters[indic.name]
                multi_index_tuples.append((
                    asset_cluster1, asset_cluster2, asset, 
                    indic_cluster1, indic_cluster2, 
                    indic.name, param_str
                ))

    return pd.MultiIndex.from_tuples( # type: ignore
        multi_index_tuples,
        names=["AssetCluster", "AssetSubCluster", "Asset", "IndicCluster", "IndicSubCluster", "Indicator", "Param"]
    )

def perform_clustering(
    distance_matrix: DataFrameFloat, 
    num_clusters: int, 
    method: str = 'complete', 
    criterion: str='maxclust'
    ) -> ArrayFloat:
    
    linkage_matrix = linkage(squareform(distance_matrix), method=method)
    return fcluster(linkage_matrix, num_clusters, criterion=criterion)

def compute_linkage_matrix(
    corr_matrix: DataFrameFloat, 
    method:str = 'average'
    ) -> ArrayFloat:
    pairwise_distances = calculate_pairwise_distances(corr_matrix)
    condensed_distances = squareform(pairwise_distances.nparray)
    return linkage(condensed_distances, method=method)

def create_cluster_dict(assets: list[str], clusters: ArrayFloat) -> dict[str, list[str]]:
    cluster_dict: dict[str, list[str]] = {}
    for asset, cluster in zip(assets, clusters):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(asset)
    return {k: cluster_dict[k] for k in sorted(cluster_dict)}

def cluster_subdivision(
    returns_df: DataFrameFloat, 
    assets: list[str], 
    max_subclusters: int, 
    method: str = 'ward'
    ) -> list[str] | dict[str, list[str]]:

    if len(assets) <= 1:
        return assets
    sub_assets_group = DataFrameFloat(data=returns_df[assets])
    sub_distance_matrix: DataFrameFloat = calculate_distance_matrix(returns_df=sub_assets_group)
    sub_clusters: ArrayFloat = perform_clustering(distance_matrix=sub_distance_matrix, num_clusters=max_subclusters, method=method)
    return create_cluster_dict(assets=assets, clusters=sub_clusters)

def recursive_subdivision(
    returns_df: DataFrameFloat, 
    cluster_dict: dict[str, list[str]], 
    max_subclusters: int
) -> dict[str, dict[str, list[str]]]:
    for main_cluster, assets in cluster_dict.items():
        if len(assets) > 1:
            subcluster_dict = cluster_subdivision(
                returns_df=returns_df, 
                assets=assets, 
                max_subclusters=max_subclusters)
            cluster_dict[main_cluster] = subcluster_dict
    return cluster_dict

def generate_static_clusters(
    returns_df: DataFrameFloat, 
    max_clusters: int = 3, 
    max_subclusters: int = 1
) -> dict[str, dict[str, list[str]]]:

    distance_matrix: DataFrameFloat = calculate_distance_matrix(returns_df=returns_df)
    main_clusters: ArrayFloat = perform_clustering(distance_matrix=distance_matrix, num_clusters=max_clusters)
    main_cluster_dict: dict[str, list[str]] = create_cluster_dict(assets=list(returns_df.columns), clusters=main_clusters)
    cluster_dict: dict[str, dict[str, list[str]]] = recursive_subdivision(returns_df=returns_df, cluster_dict=main_cluster_dict, max_subclusters=max_subclusters)

    return flatten_singleton_clusters(cluster_dict=cluster_dict)


def flatten_singleton_clusters(cluster_dict: dict[str, list[str]]) -> DictVariableDepth:

    new_cluster_dict = {}
    
    for key, value in cluster_dict.items():
        if isinstance(value, dict):
            flattened_value = flatten_singleton_clusters(value)
            
            if len(flattened_value) == 1:
                new_cluster_dict[key] = [item for sublist in flattened_value.values() for item in sublist]
            elif all(isinstance(sub_value, list) and len(sub_value) == 1 for sub_value in flattened_value.values()):
                new_cluster_dict[key] = [item for sublist in flattened_value.values() for item in sublist]
            else:
                new_cluster_dict[key] = flattened_value
        else:
            new_cluster_dict[key] = value
    return new_cluster_dict