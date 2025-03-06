from numpy import argsort, fill_diagonal, nan, nanmax, nanmin, quantile, where, zeros_like

from outquantlab.metrics import PERCENTAGE_FACTOR, get_overall_mean
from outquantlab.typing_conventions import (
    ArrayFloat,
    ArrayInt,
    DataFrameFloat,
    Float32,
)


def fill_correlation_matrix(corr_matrix: ArrayFloat) -> ArrayFloat:
    fill_diagonal(a=corr_matrix, val=nan)
    return corr_matrix


def format_returns(returns_array: ArrayFloat, limit: float) -> ArrayFloat:
    lower_threshold: ArrayFloat = quantile(a=returns_array, q=limit, axis=0)
    upper_threshold: ArrayFloat = quantile(a=returns_array, q=1 - limit, axis=0)

    limited_returns_array: ArrayFloat = where(
        (returns_array >= lower_threshold) & (returns_array <= upper_threshold),
        returns_array,
        nan,
    )

    return limited_returns_array * PERCENTAGE_FACTOR

def prepare_sunburst_data(
    cluster_dict: dict[str, list[str]],
    parent_label: str = "",
    labels: list[str] | None = None,
    parents: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    if labels is None:
        labels = []
    if parents is None:
        parents = []

    for key, value in cluster_dict.items():
        current_label: str = parent_label + str(key) if parent_label else str(key)
        if isinstance(value, dict):
            prepare_sunburst_data(
                cluster_dict=value,
                parent_label=current_label,
                labels=labels,
                parents=parents,
            )
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

def sort_dataframe(
    df: DataFrameFloat, use_final: bool = False, ascending: bool = True
) -> DataFrameFloat:
    if use_final:
        sorted_indices: ArrayInt = argsort(a=df.get_array()[-1, :])
    else:
        mean_values: ArrayFloat = get_overall_mean(array=df.get_array(), axis=0)
        sorted_indices: ArrayInt = argsort(a=mean_values)
    if not ascending:
        sorted_indices = sorted_indices[::-1]

    sorted_data: ArrayFloat = df.get_array()[:, sorted_indices]
    sorted_columns: list[str] = [df.columns[i] for i in sorted_indices]

    return DataFrameFloat(data=sorted_data, columns=sorted_columns, index=df.dates)


def normalize_data_for_colormap(data: ArrayFloat):
    z_min: Float32 = nanmin(data)
    z_max: Float32 = nanmax(data)
    normalized_data = (
        (data - z_min) / (z_max - z_min) if z_max > z_min else zeros_like(a=data)
    )
    return normalized_data
