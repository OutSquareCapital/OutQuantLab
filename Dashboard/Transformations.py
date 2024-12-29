import numpy as np
import pandas as pd
from Metrics import calculate_overall_mean
from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat, DictVariableDepth, PERCENTAGE_FACTOR, Float32, ArrayInt

def format_returns(returns_df: DataFrameFloat, limit: float) -> DataFrameFloat:
    lower_threshold = SeriesFloat(data=returns_df.quantile(q=limit, axis=0) ) 
    upper_threshold = SeriesFloat(data=returns_df.quantile(q=1-limit, axis=0) )
    
    limited_returns_array: ArrayFloat = np.where(
        (returns_df >= lower_threshold) & (returns_df <= upper_threshold), 
        returns_df, 
        np.nan)

    formatted_returns_df = DataFrameFloat(
        data=limited_returns_array, 
        columns=returns_df.columns, 
        index=returns_df.dates
        )

    return formatted_returns_df * PERCENTAGE_FACTOR

def convert_series_multiindex_labels(series: SeriesFloat) -> SeriesFloat:
    if isinstance(series.index, pd.MultiIndex):
        series.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(object=idx) for idx in series.index]
    return series

def convert_dataframe_multiindex_labels(df: DataFrameFloat) -> DataFrameFloat:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(map(str, col)) if isinstance(col, tuple) else str(object=col) for col in df.columns]
    if isinstance(df.index, pd.MultiIndex):
        df.index = ["_".join(map(str, idx)) if isinstance(idx, tuple) else str(object=idx) for idx in df.index]
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
        sorted_indices: ArrayInt = np.argsort(a=df.nparray[:, -1])
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