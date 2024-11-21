from joblib import Parallel, delayed
from typing import Tuple
from tqdm import tqdm
import numpy as np

def create_progress_bar(total:int, description="Processing"):

    pbar = tqdm(total=total, desc=description)

    def update_progress():
        pbar.update(1)

    return pbar, update_progress

def process_param(func, data_array, param):

    return func(data_array, **param)

def initialize_signals_array(prices_array: np.ndarray,
                            log_returns_array: np.ndarray,
                            indicators_and_params: dict,
                            asset_names: list
                            ) -> Tuple[np.ndarray, dict, any, any, int, int, int, int]:
    
    total_days = prices_array.shape[0]

    num_assets = len(asset_names)
    num_params = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
    num_indicators = len(indicators_and_params)
    total_return_streams = num_assets * num_params

    signals_array = np.full((total_days, total_return_streams), np.nan, dtype=np.float32)

    data_arrays = {
        'returns_array': log_returns_array,
        'prices_array': prices_array
    }

    print(f'processing {num_params} params from {num_indicators} indicators on {num_assets} assets, for a total of {total_return_streams} individuals strategies...')

    return signals_array, data_arrays,  num_indicators

def calculate_signals_params(signals_array: np.ndarray,
                            data_arrays: dict,
                            indicators_and_params: dict,
                            num_indicators: int
                            ) -> np.ndarray:
    
    signal_col_index = 0

    # Créer la barre de progression
    pbar, update_progress = create_progress_bar(num_indicators, description="Calculating signals")

    try:
        # Parallélisation des calculs sur les paramètres
        for func, array_type, params in indicators_and_params.values():
            # Récupérer le tableau réel via `array_type`
            data_array = data_arrays[array_type]

            # Paralléliser sur les paramètres de cet indicateur
            results = Parallel(n_jobs=-1, backend='threading')(delayed(process_param)(
                func, data_array, param) for param in params)

            # Empiler les résultats et les insérer dans l'array final
            results_stacked = np.hstack(results)
            num_cols = results_stacked.shape[1]
            signals_array[:, signal_col_index:signal_col_index + num_cols] = results_stacked

            # Mise à jour de l'index de colonne
            signal_col_index += num_cols

            # Mettre à jour la progression après chaque indic (pour tous les actifs)
            update_progress()

    finally:
        pbar.close()

    return signals_array

def calculate_strategy_signals(prices_array: np.ndarray, 
                            log_returns_array: np.ndarray,
                            asset_names: list,
                            indicators_and_params: dict,
                            ) -> np.ndarray:

    (
    signals_array, 
    data_arrays, 
    num_indicators) = initialize_signals_array(prices_array, 
                                                log_returns_array, 
                                                indicators_and_params, 
                                                asset_names)

    return calculate_signals_params(signals_array,
                                    data_arrays,
                                    indicators_and_params,
                                    num_indicators)
