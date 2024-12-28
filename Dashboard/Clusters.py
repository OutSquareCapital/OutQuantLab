from scipy.cluster.hierarchy import linkage, fcluster # type: ignore
from scipy.spatial.distance import squareform
from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth

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