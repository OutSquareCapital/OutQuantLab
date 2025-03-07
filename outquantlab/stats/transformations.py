from numpy import (
    fill_diagonal,
    nan,
    nanmax,
    nanmin,
    zeros_like,
)

from outquantlab.typing_conventions import (
    ArrayFloat,
    Float32,
)


def fill_correlation_matrix(corr_matrix: ArrayFloat) -> ArrayFloat:
    fill_diagonal(a=corr_matrix, val=nan)
    return corr_matrix

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

def normalize_data_for_colormap(data: ArrayFloat):
    z_min: Float32 = nanmin(data)
    z_max: Float32 = nanmax(data)
    normalized_data = (
        (data - z_min) / (z_max - z_min) if z_max > z_min else zeros_like(a=data)
    )
    return normalized_data
