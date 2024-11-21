from joblib import Parallel, delayed
import numpy as np
from Process_Data import calculate_volatility_adjusted_returns
from .Backtest_Initialization import create_progress_bar, initialize_returns_array

def process_param(func, data_array, adjusted_returns_array, param):

    # Calculer le signal
    signal = func(data_array, **param)

    # Multiplier le signal par les adjusted returns
    return signal * adjusted_returns_array

def calculate_strategy_returns(signals_array: np.ndarray,
                             data_arrays: dict,
                             indicators_and_params: dict,
                             adjusted_returns_array: np.ndarray,
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
                func, data_array, adjusted_returns_array, param) for param in params)

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


def transform_signals_into_returns(prices_array: np.ndarray, 
                                    log_returns_array: np.ndarray,
                                    pct_returns_array: np.ndarray, 
                                    hv_array: np.ndarray, 
                                    asset_names: list,
                                    indicators_and_params: dict,
                                    vol_adjustement:int = 15,
                                    ) -> np.ndarray:
    
    volatility_adjusted_returns = calculate_volatility_adjusted_returns(
                                                                        pct_returns_array, 
                                                                        hv_array, 
                                                                        vol_adjustement
                                                                        )
    (
    signals_array, 
    data_arrays, 
    num_indicators) = initialize_returns_array(prices_array, 
                                                log_returns_array, 
                                                indicators_and_params, 
                                                asset_names)

    return calculate_strategy_returns(signals_array,
                                    data_arrays,
                                    indicators_and_params,
                                    volatility_adjusted_returns,
                                    num_indicators)