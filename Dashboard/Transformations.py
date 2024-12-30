import numpy as np
import pandas as pd
from Metrics import calculate_overall_mean
from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat, DictVariableDepth, PERCENTAGE_FACTOR, Float32, ArrayInt

def fill_correlation_matrix(corr_matrix: ArrayFloat) -> ArrayFloat:
    np.fill_diagonal(a=corr_matrix, val=np.nan)
    return corr_matrix

def format_returns(returns_array: ArrayFloat, limit: float) -> ArrayFloat:
    lower_threshold: ArrayFloat = np.quantile(a=returns_array, q=limit, axis=0)
    upper_threshold: ArrayFloat = np.quantile(a=returns_array, q=1-limit, axis=0)

    limited_returns_array: ArrayFloat = np.where(
        (returns_array >= lower_threshold) & (returns_array <= upper_threshold), 
        returns_array, 
        np.nan)

    return limited_returns_array * PERCENTAGE_FACTOR

def convert_multiindex_to_labels(df: DataFrameFloat) -> list[str]:
    multi_index: pd.MultiIndex = df.columns # type: ignore
    flattened_index: pd.Index = multi_index.map(mapper="_".join) # type: ignore
    labels: list[str] = flattened_index.to_list()
    return labels

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
        current_label: str = parent_label + str(key) if parent_label else str(key)
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

def sort_series(
    series: SeriesFloat, 
    ascending: bool = True
    ) -> SeriesFloat:
    if ascending:
        sorted_array: ArrayFloat = np.sort(a=series.nparray)
    else:
        sorted_array: ArrayFloat = np.sort(a=series.nparray)[::-1]
    return SeriesFloat(data=sorted_array, index=series.names)

def sort_dataframe(
    df: DataFrameFloat, 
    use_final: bool = False, 
    ascending: bool = True
    ) -> DataFrameFloat:
    if use_final:
        sorted_indices: ArrayInt = np.argsort(a=df.nparray[-1, :])
    else:
        mean_values: ArrayFloat = calculate_overall_mean(array=df.nparray, axis=0)
        sorted_indices: ArrayInt = np.argsort(a=mean_values)
    if not ascending:
        sorted_indices = sorted_indices[::-1]

    sorted_data: ArrayFloat = df.nparray[:, sorted_indices]
    sorted_columns: list[str] = [df.columns[i] for i in sorted_indices]

    return DataFrameFloat(data=sorted_data, columns=sorted_columns, index=df.dates)

def normalize_data_for_colormap(data: ArrayFloat):
    z_min: Float32 = np.nanmin(data)
    z_max: Float32 = np.nanmax(data)
    normalized_data = (data - z_min) / (z_max - z_min) if z_max > z_min else np.zeros_like(a=data)
    return normalized_data