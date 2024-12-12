import numpy as np

def renormalize_weights(weights: np.ndarray, returns: np.ndarray) -> np.ndarray:

    sum_weights = np.nansum(weights, axis=1)

    available_assets_count = np.sum(~np.isnan(returns), axis=1)

    sum_weights[sum_weights == 0] = np.nan

    renormalized_weights = (weights.T / sum_weights).T * available_assets_count[:, np.newaxis]

    return np.nan_to_num(renormalized_weights)