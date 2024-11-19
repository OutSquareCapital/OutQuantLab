import numpy as np

def renormalize_weights(weights: np.ndarray, returns: np.ndarray) -> np.ndarray:

    # Calculer la somme des poids par ligne (axis=1)
    sum_weights = np.nansum(weights, axis=1)

    # Calculer le nombre d'actifs disponibles pour chaque ligne (axis=1)
    available_assets_count = np.sum(~np.isnan(returns), axis=1)

    # Éviter la division par 0 en remplaçant les sum_weights == 0 par NaN temporairement
    sum_weights[sum_weights == 0] = np.nan

    # Renormaliser les poids en fonction du nombre d'actifs disponibles
    renormalized_weights = (weights.T / sum_weights).T * available_assets_count[:, np.newaxis]

    # Remplacer les NaN restants par 0 (issus des lignes avec aucun actif ou division par zéro)
    renormalized_weights = np.nan_to_num(renormalized_weights)

    return renormalized_weights