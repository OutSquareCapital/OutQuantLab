import numpy as np
import pandas as pd
from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat, DictVariableDepth
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, leaves_list # type: ignore

def convert_series_multiindex_labels(series: SeriesFloat) -> SeriesFloat:
    if isinstance(series.index, pd.MultiIndex):
        series.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(idx) for idx in series.index]
    return series

def convert_dataframe_multiindex_labels(df: DataFrameFloat) -> DataFrameFloat:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(map(str, col)) if isinstance(col, tuple) else str(col) for col in df.columns]
    if isinstance(df.index, pd.MultiIndex):
        df.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(idx) for idx in df.index]
    return df

def compute_linkage_matrix(corr_matrix: DataFrameFloat) -> ArrayFloat:

    pairwise_distances = DataFrameFloat(1 - corr_matrix.abs())
    condensed_distances = squareform(pairwise_distances.nparray)
    return linkage(condensed_distances, method='average')

def sort_correlation_matrix(corr_matrix: DataFrameFloat) -> DataFrameFloat:

    linkage_matrix = compute_linkage_matrix(corr_matrix)
    ordered_indices = leaves_list(linkage_matrix)

    sorted_corr_matrix = corr_matrix.iloc[ordered_indices, ordered_indices]
    np.fill_diagonal(sorted_corr_matrix.values, np.nan) # type: ignore

    return sorted_corr_matrix # type: ignore

def prepare_sunburst_data(
    cluster_dict:DictVariableDepth, 
    parent_label:str="", 
    labels: list[str]|None = None, 
    parents: list[str]|None = None
    ) -> tuple[list[str], list[str]]:

    if labels is None:
        labels = []
    if parents is None:
        parents = []
        
    for key, value in cluster_dict.items():
        current_label = parent_label + str(key) if parent_label else str(key)
        if isinstance(value, dict):
            prepare_sunburst_data(value, current_label, labels, parents) # type: ignore
        else:
            for asset in value:
                labels.append(asset)
                parents.append(current_label)
        if parent_label:
            labels.append(current_label)
            parents.append(parent_label)
        else:
            labels.append(current_label)
            parents.append("")
            
    return labels, parents

def sort_series(data: SeriesFloat, ascending: bool = True) -> SeriesFloat:
    return data.sort_values(ascending=ascending) # type: ignore

def sort_dataframe(data: DataFrameFloat, use_final: bool = False, ascending: bool = True) -> DataFrameFloat:
    if use_final:
        return data.sort_values(by=data.dates[-1], axis=1, ascending=ascending) # type: ignore
    else:
        sorted_data = data.mean().sort_values(ascending=ascending)
        return data[sorted_data.index] # type: ignore

def normalize_data_for_colormap(data: ArrayFloat):

    z_min = np.nanmin(data)
    z_max = np.nanmax(data)
    normalized_data = (data - z_min) / (z_max - z_min) if z_max > z_min else np.zeros_like(data)
    return normalized_data