import numpy as np
import pandas as pd
from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat, DictVariableDepth

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
    return data.sort_values(ascending=ascending)

def sort_dataframe(data: DataFrameFloat, use_final: bool = False, ascending: bool = True) -> DataFrameFloat:
    if use_final:
        return data.sort_values(by=data.dates[-1], axis=1, ascending=ascending)
    else:
        sorted_data = data.mean().sort_values(ascending=ascending)
        return data[sorted_data.index]

def normalize_data_for_colormap(data: ArrayFloat):

    z_min = np.nanmin(data)
    z_max = np.nanmax(data)
    normalized_data = (data - z_min) / (z_max - z_min) if z_max > z_min else np.zeros_like(data)
    return normalized_data