import numexpr as ne
from Infrastructure import Fast_Tools as ft
import numpy as np
from Process_Data import calculate_volatility_adjusted_returns

def calculate_and_extend_volatility_adjusted_returns(
    pct_returns_array: np.ndarray,
    signals_array,
    hv_array: np.ndarray,
    vol_adjustement: int = 15
) -> np.ndarray:
    
    # Étape 1 : Calcul des rendements ajustés par la volatilité
    volatility_adjusted_returns = calculate_volatility_adjusted_returns(
                                                                        pct_returns_array, 
                                                                        hv_array, 
                                                                        vol_adjustement
                                                                        )
    
    # Dériver num_repeats à partir des shapes
    num_repeats = signals_array.shape[1] // volatility_adjusted_returns.shape[1]

    return np.tile(volatility_adjusted_returns, (1, num_repeats)).astype(np.float32)

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


def apply_signals_on_adjusted_returns(
    extended_volatility_adjusted_returns: np.ndarray, 
    signals_array: np.ndarray, 
    long_bias: bool = False
) -> np.ndarray:
    
    if long_bias:
        signals_array = assign_signal_bias(signals_array)
        
    signals_shifted = ft.shift_array(signals_array)

    out_array = np.empty_like(extended_volatility_adjusted_returns, dtype=np.float32)
    
    return ne.evaluate('extended_volatility_adjusted_returns * signals_shifted', out=out_array)

def calculate_strategy_returns(
    pct_returns_array: np.ndarray, 
    signals_array: np.ndarray, 
    hv_array: np.ndarray, 
    vol_adjustement: int = 15,
    long_bias: bool = False
) -> np.ndarray:

    extended_volatility_adjusted_returns = calculate_and_extend_volatility_adjusted_returns(
                                                                                            pct_returns_array,
                                                                                            signals_array,
                                                                                            hv_array,
                                                                                            vol_adjustement)

    return apply_signals_on_adjusted_returns(
            extended_volatility_adjusted_returns, 
            signals_array, 
            long_bias)