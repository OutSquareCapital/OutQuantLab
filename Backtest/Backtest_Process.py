from joblib import Parallel, delayed
import numpy as np
from .Backtest_Initialization import initialize_data_array, initialize_signals_array


def process_param(func, data_array, adjusted_returns_array, param):

    # Calculer le signal
    signal = func(data_array, **param)

    # Multiplier le signal par les adjusted returns
    return signal * adjusted_returns_array

def calculate_strategy_returns(
                            signals_array: np.ndarray,
                            data_arrays: dict,
                            indicators_and_params: dict,
                            adjusted_returns_array: np.ndarray,
                            progress_callback: callable
                            ) -> np.ndarray:

    signal_col_index = 0
    total_columns = signals_array.shape[1]
    total_steps = 70 - 10

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

        # Mise à jour de la progression
        progress = 10 + int(total_steps * signal_col_index / total_columns)
        progress_callback(progress, f"Backtesting Strategies: {signal_col_index}/{total_columns}...")

    return signals_array


def transform_signals_into_returns(prices_array: np.ndarray, 
                                    log_returns_array: np.ndarray,
                                    volatility_adjusted_pct_returns_array: np.ndarray, 
                                    asset_names: list,
                                    indicators_and_params: dict,
                                    progress_callback: callable
                                    ) -> np.ndarray:
    
    data_arrays = initialize_data_array(prices_array,
                                        log_returns_array)

    signals_array = initialize_signals_array(
                                            prices_array, 
                                            indicators_and_params, 
                                            asset_names
                                            )

    return calculate_strategy_returns(
                                    signals_array,
                                    data_arrays,
                                    indicators_and_params,
                                    volatility_adjusted_pct_returns_array,
                                    progress_callback
                                    )