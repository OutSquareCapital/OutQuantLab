import pandas as pd
import numpy as np
import numexpr as ne
from joblib import Parallel, delayed
from Process_Data import calculate_volatility_adjusted_returns
from typing import Tuple
from Infrastructure import Fast_Tools as ft
from tqdm import tqdm

def create_progress_bar(total:int, description="Processing"):

    pbar = tqdm(total=total, desc=description)

    def update_progress():
        pbar.update(1)

    return pbar, update_progress


def process_param(func, data_array, param):

    return func(data_array, **param)

class SignalsApplication :

    def extend_volatility_adjusted_returns(
        volatility_adjusted_returns: np.ndarray,
        num_repeats: int
    ) -> np.ndarray:

        return np.tile(volatility_adjusted_returns, (1, num_repeats)).astype(np.float32)

    @staticmethod
    def calculate_and_extend_volatility_adjusted_returns(
        pct_returns_array: np.ndarray, 
        hv_array: np.ndarray, 
        num_repeats: int,
        vol_adjustement: int = 15
    ) -> np.ndarray:
        
        # Étape 1 : Calcul des rendements ajustés par la volatilité
        volatility_adjusted_returns = calculate_volatility_adjusted_returns(
            pct_returns_array, 
            hv_array, 
            vol_adjustement
        )

        return SignalsApplication.extend_volatility_adjusted_returns(
            volatility_adjusted_returns, 
            num_repeats)

    # A VOIR COMMENT UTILISER POUR LES 2 EN MEME TEMPS
    def assign_signal_bias(data_array:np.ndarray, long=True):
        if long:
            # Remplacer les valeurs négatives par 0 pour le tableau "Long"
            result_array = np.where((data_array >= 0) | np.isnan(data_array), data_array, 0)
        else:
            # Remplacer les valeurs positives par 0 pour le tableau "Short"
            result_array = np.where((data_array < 0) | np.isnan(data_array), data_array, 0)
        
        # Concatenation des deux tableaux (colonnes d'origine + nouvelles colonnes)
        #result_array = np.concatenate([data_long_array, data_short_array], axis=1)
        
        return result_array

    @staticmethod
    def apply_signals_on_adjusted_returns(
        extended_volatility_adjusted_returns: np.ndarray, 
        signals_array: np.ndarray, 
        long_bias: bool = False
    ) -> np.ndarray:
        
        if long_bias:
            signals_array = SignalsApplication.assign_signal_bias(signals_array)
            
        signals_shifted = ft.shift_array(signals_array)

        out_array = np.empty_like(extended_volatility_adjusted_returns, dtype=np.float32)
        
        return ne.evaluate('extended_volatility_adjusted_returns * signals_shifted', out=out_array)


class SignalsProcessing:


    @staticmethod
    def initialize_signals_array(prices_array: np.ndarray,
                                log_returns_array: np.ndarray,
                                indicators_and_params: dict,
                                asset_names: list) -> Tuple[np.ndarray, dict, any, any, int, int, int, int]:
        
        total_days = prices_array.shape[0]

        # Calcul des métriques nécessaires
        num_assets = len(asset_names)
        num_params = sum(len(params) for _, (_, _, params) in indicators_and_params.items())
        num_indicators = len(indicators_and_params)
        total_return_streams = num_assets * num_params
        num_repeats = total_return_streams // num_assets

        # Initialiser un array pour stocker les signaux
        signals_array = np.full((total_days, total_return_streams), np.nan, dtype=np.float32)

        # Dictionnaire de correspondance pour accéder aux tableaux réels
        data_arrays = {
            'returns_array': log_returns_array,
            'prices_array': prices_array
        }

        print(f'processing {num_params} params from {num_indicators} indicators on {num_assets} assets, for a total of {total_return_streams} individuals strategies...')

        return signals_array, data_arrays,  num_indicators, num_repeats


    @staticmethod
    def calculate_signals_array(signals_array: np.ndarray,
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

    @staticmethod
    def calculate_strategy_returns(
        pct_returns_array: np.ndarray, 
        signals_array: np.ndarray, 
        hv_array: np.ndarray, 
        num_repeats: int,
        vol_adjustement: int = 15,
        long_bias: bool = False
    ) -> np.ndarray:

        extended_volatility_adjusted_returns = SignalsApplication.calculate_and_extend_volatility_adjusted_returns(
            pct_returns_array, 
            hv_array, 
            num_repeats,
            vol_adjustement)

        return SignalsApplication.apply_signals_on_adjusted_returns(
                extended_volatility_adjusted_returns, 
                signals_array, 
                long_bias)

    @staticmethod
    def data_arrays_to_dataframe(raw_adjusted_returns_array: np.ndarray, 
                                 signals_array: np.ndarray, 
                                 dates_index: pd.Index, 
                                 indicators_and_params: dict, 
                                 asset_names: list) -> tuple[pd.DataFrame, pd.DataFrame]:

        column_names = []
        # Générer les noms de colonnes basés sur les actifs et les stratégies
        for indicator_name, (_, _, params) in indicators_and_params.items():
            for param in params:
                param_str = ''.join([f"{k}{v}" for k, v in param.items()])
                for asset in asset_names:
                    column_names.append(f"{asset}_{indicator_name}_{param_str}")

        adjusted_returns_df = pd.DataFrame(raw_adjusted_returns_array, 
                                           index=dates_index, 
                                           columns=column_names, 
                                           dtype=np.float32)
        signals_df = pd.DataFrame(signals_array, 
                                  index=dates_index, 
                                  columns=column_names, 
                                  dtype=np.float32)

        return signals_df, adjusted_returns_df

    
    @staticmethod
    def trading_signals(
                        prices_array: np.ndarray, 
                        log_returns_array: np.ndarray,
                        pct_returns_array: np.ndarray, 
                        hv_array: np.ndarray, 
                        asset_names: list,
                        dates_index: pd.Index,
                        indicators_and_params: dict,
                        vol_adjustement:int = 15,
                        long_bias_adjustment: bool = False
                        ) -> tuple[pd.DataFrame, pd.DataFrame]:
        
        (signals_array, 
        data_arrays, 
        num_indicators,
        num_repeats) = SignalsProcessing.initialize_signals_array(  prices_array, 
                                                                    log_returns_array, 
                                                                    indicators_and_params, 
                                                                    asset_names)

        signals_array = SignalsProcessing.calculate_signals_array(signals_array,
                                                                data_arrays,
                                                                indicators_and_params,
                                                                num_indicators)
        

        raw_adjusted_returns_array = SignalsProcessing.calculate_strategy_returns(
                                                                            pct_returns_array, 
                                                                            signals_array, 
                                                                            hv_array, 
                                                                            num_repeats,
                                                                            vol_adjustement, 
                                                                            long_bias_adjustment)
        
        signals_df, raw_adjusted_returns_df = SignalsProcessing.data_arrays_to_dataframe(
                                                                                    raw_adjusted_returns_array, 
                                                                                    signals_array, 
                                                                                    dates_index, 
                                                                                    indicators_and_params, 
                                                                                    asset_names)

        print('strategies processed!')

        return signals_df, raw_adjusted_returns_df