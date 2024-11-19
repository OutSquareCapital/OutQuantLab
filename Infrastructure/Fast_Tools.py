import numpy as np
from joblib import Parallel, delayed
import pandas as pd

def shift_array(returns_array: np.ndarray) -> np.ndarray:
    shifted_array = np.empty_like(returns_array, dtype=np.float32)
    shifted_array[1:, :] = returns_array[:-1, :]
    shifted_array[:1, :] = np.nan
    return shifted_array

def snapshot_at_intervals(prices_array: np.ndarray, snapshot_interval: int) -> np.ndarray:

    snapshot_indices = np.arange(0, prices_array.shape[0], snapshot_interval)

    snapshots = prices_array[snapshot_indices]

    repeated_snapshots = np.repeat(snapshots, snapshot_interval, axis=0)

    repeated_snapshots = repeated_snapshots[:prices_array.shape[0]]

    return repeated_snapshots

def process_in_blocks_parallel_numpy(array, block_size, func, *args, **kwargs):
    """
    Applique une fonction donnée en parallèle sur des blocs de colonnes d'un array.
    
    Args:
        array (np.ndarray): Tableau 2D de données.
        block_size (int): Nombre de colonnes par bloc.
        func (callable): Fonction à appliquer sur chaque bloc.
        *args: Arguments supplémentaires pour la fonction.
        **kwargs: Arguments nommés supplémentaires pour la fonction.
    
    Returns:
        np.ndarray: Résultat final après application de la fonction sur chaque bloc.
    """
    num_cols = array.shape[1]
    
    # Parallélisation sur les blocs de colonnes en appelant la fonction 'func' sur chaque bloc
    results = Parallel(n_jobs=-1, backend='threading')(
        delayed(func)(array[:, start_col:min(start_col + block_size, num_cols)], *args, **kwargs)
        for start_col in range(0, num_cols, block_size)
    )

    # Reconstruction finale de l'array
    final_result = np.hstack(results)
    return final_result

def process_in_blocks_parallel_pandas(df, block_size, func, *args, **kwargs):

    num_cols = df.shape[1]
    results = Parallel(n_jobs=-1, backend='threading')(
        delayed(func)(df.iloc[:, start_col:min(start_col + block_size, num_cols)], *args, **kwargs)
        for start_col in range(0, num_cols, block_size)
    )

    # Combinaison des résultats en un DataFrame
    final_result = pd.concat(results, axis=1)
    final_result.index = df.index
    final_result.columns = df.columns
    return final_result
