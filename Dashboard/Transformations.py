import numpy as np
import pandas as pd
import re
from collections import defaultdict
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, leaves_list

def convert_series_multiindex_labels(series):
    if isinstance(series.index, pd.MultiIndex):
        series.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(idx) for idx in series.index]
    return series

def convert_dataframe_multiindex_labels(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(map(str, col)) if isinstance(col, tuple) else str(col) for col in df.columns]
    if isinstance(df.index, pd.MultiIndex):
        df.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(idx) for idx in df.index]
    return df



def compute_linkage_matrix(corr_matrix: pd.DataFrame) -> np.ndarray:

    pairwise_distances = 1 - corr_matrix.abs()
    condensed_distances = squareform(pairwise_distances.values)
    return linkage(condensed_distances, method='average')

def sort_correlation_matrix(corr_matrix) -> pd.DataFrame:

    linkage_matrix = compute_linkage_matrix(corr_matrix)
    ordered_indices = leaves_list(linkage_matrix)

    sorted_corr_matrix = corr_matrix.iloc[ordered_indices, ordered_indices]
    np.fill_diagonal(sorted_corr_matrix.values, np.nan)

    return sorted_corr_matrix

def convert_params_to_3d(sharpe_ratios_df, param1, param2):

    sharpe_dict = defaultdict(list)

    for index, row in sharpe_ratios_df.iterrows():
        param1_value, param2_value = extract_params_from_name(index, param1, param2)
        if param1_value is not None and param2_value is not None:
            sharpe_dict[(param1_value, param2_value)].append(row['Sharpe Ratio'])
    x_vals = []
    y_vals = []
    z_vals = []
    for (p1, p2), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(np.nanmean(sharpe_list))
    
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)

    x_unique = np.unique(x_vals)
    y_unique = np.unique(y_vals)
    X, Y = np.meshgrid(x_unique, y_unique)
    Z = np.full_like(X, np.nan, dtype=np.float32)

    for i in range(len(x_vals)):
        x_idx = np.where(x_unique == x_vals[i])[0][0]
        y_idx = np.where(y_unique == y_vals[i])[0][0]
        Z[y_idx, x_idx] = z_vals[i]

    return X, Y, Z

def convert_params_to_4d(sharpe_ratios_df, params):

    sharpe_dict = defaultdict(list)

    for index, row in sharpe_ratios_df.iterrows():
        param_values = extract_all_params_from_name(index, params)
        if all(param_values):
            key = tuple(param_values[:3])
            sharpe_dict[key].append(row['Sharpe Ratio'])
    x_vals = []
    y_vals = []
    z_vals = []
    sharpe_means = []

    for (p1, p2, p3), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(p3)
        sharpe_means.append(np.nanmean(sharpe_list))

    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)
    sharpe_means = np.array(sharpe_means)

    return x_vals, y_vals, z_vals, sharpe_means

def extract_params_from_name(name: str, param1: str, param2: str) -> tuple:

    pattern1 = re.compile(f"{param1}(\\d+)")
    pattern2 = re.compile(f"{param2}(\\d+)")
    
    match1 = pattern1.search(name)
    match2 = pattern2.search(name)
    
    param1_value = int(match1.group(1)) if match1 else None
    param2_value = int(match2.group(1)) if match2 else None
    
    return param1_value, param2_value

def extract_all_params_from_name(name: str, params: list) -> list:

    extracted_values = []
    for param in params:
        pattern = re.compile(f"{param}(\\d+)")
        match = pattern.search(name)
        extracted_values.append(int(match.group(1)) if match else None)
    
    return extracted_values

def prepare_sunburst_data(cluster_dict, parent_label="", labels=None, parents=None):

    if labels is None:
        labels = []
    if parents is None:
        parents = []
        
    for key, value in cluster_dict.items():
        current_label = parent_label + str(key) if parent_label else str(key)
        if isinstance(value, dict):
            prepare_sunburst_data(value, current_label, labels, parents)
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

def sort_series(data: pd.Series, ascending: bool = True) -> pd.Series:
    return data.sort_values(ascending=ascending)

def sort_dataframe(data: pd.DataFrame, use_final: bool = False, ascending: bool = True) -> pd.DataFrame:
    if use_final:
        return data.sort_values(by=data.index[-1], axis=1, ascending=ascending)
    else:
        sorted_data = data.mean().sort_values(ascending=ascending)
        return data[sorted_data.index]

def normalize_data_for_colormap(data: np.ndarray):

    z_min = np.nanmin(data)
    z_max = np.nanmax(data)
    normalized_data = (data - z_min) / (z_max - z_min) if z_max > z_min else np.zeros_like(data)
    return normalized_data