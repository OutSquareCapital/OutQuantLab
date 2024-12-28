from scipy.cluster.hierarchy import linkage, fcluster, leaves_list # type: ignore
from scipy.spatial.distance import squareform
from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth
from Database import load_config_file, save_config_file
import pandas as pd
from .Indicators import Indicator

class ClustersTree:
    def __init__(self, clusters_file: str) -> None:
        self.clusters_file: str = clusters_file
        self.clusters = load_config_file(self.clusters_file)

    def update_clusters_structure(self, new_structure: DictVariableDepth) -> None:
        self.clusters = new_structure

    def map_nested_clusters_to_entities(self) -> dict[str, tuple[str, str]]:
        return {
            asset: (level1, level2)
            for level1, subclusters in self.clusters.items()
            for level2, assets in subclusters.items()
            for asset in assets
        }

    def save(self) -> None:
        save_config_file(self.clusters_file, self.clusters, indent=3)


def calculate_distance_matrix(returns_df: DataFrameFloat) -> DataFrameFloat:
    corr_matrix = returns_df.corr()
    return DataFrameFloat(1 - corr_matrix)

def perform_clustering(distance_matrix: DataFrameFloat, num_clusters: int, method: str = 'complete') -> ArrayFloat:
    linkage_matrix = linkage(squareform(distance_matrix), method=method)
    return fcluster(linkage_matrix, num_clusters, criterion='maxclust')

def create_cluster_dict(assets: list[str], clusters: ArrayFloat) -> dict[str, list[str]]:
    cluster_dict: dict[str, list[str]] = {}
    for asset, cluster in zip(assets, clusters):
        if cluster not in cluster_dict:
            cluster_dict[cluster] = []
        cluster_dict[cluster].append(asset)
    return {k: cluster_dict[k] for k in sorted(cluster_dict)}



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

def cluster_subdivision(
    returns_df: DataFrameFloat, 
    assets: list[str], 
    max_subclusters: int, 
    method: str = 'ward'
    ) -> list[str] | dict[str, list[str]]:

    if len(assets) <= 1:
        return assets
    sub_assets_group = DataFrameFloat(returns_df[assets])
    sub_distance_matrix = calculate_distance_matrix(sub_assets_group)
    sub_clusters = perform_clustering(sub_distance_matrix, max_subclusters, method=method)
    return create_cluster_dict(assets, sub_clusters)

def recursive_subdivision(
    returns_df: DataFrameFloat, 
    cluster_dict: DictVariableDepth, 
    max_subclusters: int, 
    max_subsubclusters: int
) -> dict[str, dict[str, list[str]]]:
    for main_cluster, assets in cluster_dict.items():
        if len(assets) > 1:
            subcluster_dict = cluster_subdivision(returns_df, assets, max_subclusters)
            if max_subsubclusters:
                for sub_cluster, sub_assets in subcluster_dict.items():
                    if len(sub_assets) > 1:
                        sub_subcluster_dict = cluster_subdivision(returns_df, sub_assets, max_subsubclusters, method='average')
                        subcluster_dict[sub_cluster] = sub_subcluster_dict
            cluster_dict[main_cluster] = subcluster_dict
    return cluster_dict

def generate_static_clusters(
    returns_df: DataFrameFloat, 
    max_clusters: int = 3, 
    max_subclusters: int = 1, 
    max_subsubclusters: int = 1
) -> DictVariableDepth:
    distance_matrix = calculate_distance_matrix(returns_df)
    main_clusters = perform_clustering(distance_matrix, max_clusters)
    cluster_dict = create_cluster_dict(list(returns_df.columns), main_clusters)

    if max_subclusters:
        cluster_dict = recursive_subdivision(returns_df, cluster_dict, max_subclusters, max_subsubclusters)

    return flatten_singleton_clusters(cluster_dict)


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


def compute_linkage_matrix(corr_matrix: DataFrameFloat) -> ArrayFloat:

    pairwise_distances = DataFrameFloat(1 - corr_matrix.abs())
    condensed_distances = squareform(pairwise_distances.nparray)
    return linkage(condensed_distances, method='average')

def sort_correlation_matrix(corr_matrix: DataFrameFloat) -> DataFrameFloat:

    linkage_matrix = compute_linkage_matrix(corr_matrix)
    ordered_indices = leaves_list(linkage_matrix)

    sorted_corr_matrix = corr_matrix.iloc[ordered_indices, ordered_indices]
    np.fill_diagonal(sorted_corr_matrix.values, np.nan)

    return sorted_corr_matrix
