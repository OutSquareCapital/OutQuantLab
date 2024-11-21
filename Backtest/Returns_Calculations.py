import pandas as pd
import numpy as np
from .Apply_Signals import calculate_strategy_returns
from .Process_Signals import calculate_strategy_signals

def data_arrays_to_dataframe(raw_adjusted_returns_array: np.ndarray, 
                                dates_index: pd.Index, 
                                indicators_and_params: dict, 
                                asset_names: list
                                ) -> tuple[pd.DataFrame, pd.DataFrame]:

    column_names = []
    # Générer les noms de colonnes basés sur les actifs et les stratégies
    for indicator_name, (_, _, params) in indicators_and_params.items():
        for param in params:
            param_str = ''.join([f"{k}{v}" for k, v in param.items()])
            for asset in asset_names:
                column_names.append(f"{asset}_{indicator_name}_{param_str}")

    return pd.DataFrame(raw_adjusted_returns_array, 
                        index=dates_index, 
                        columns=column_names, 
                        dtype=np.float32)

def transform_signals_into_returns(prices_array: np.ndarray, 
                                    log_returns_array: np.ndarray,
                                    pct_returns_array: np.ndarray, 
                                    hv_array: np.ndarray, 
                                    asset_names: list,
                                    indicators_and_params: dict,
                                    vol_adjustement:int = 15,
                                    long_bias_adjustment: bool = False
                                    ) -> np.ndarray:
    
    signals_array = calculate_strategy_signals(prices_array,
                                            log_returns_array,
                                            asset_names,
                                            indicators_and_params)

    return calculate_strategy_returns(pct_returns_array,
                                        signals_array, 
                                        hv_array,
                                        vol_adjustement, 
                                        long_bias_adjustment)

def process_backtest(prices_array: np.ndarray, 
                    log_returns_array: np.ndarray,
                    pct_returns_array: np.ndarray, 
                    hv_array: np.ndarray, 
                    asset_names: list,
                    dates_index: pd.Index,
                    indicators_and_params: dict,
                    vol_adjustement:int = 15,
                    long_bias_adjustment: bool = False
                    ) -> tuple[pd.DataFrame, pd.DataFrame]:

    raw_adjusted_returns_array = transform_signals_into_returns(prices_array,
                                                                log_returns_array,
                                                                pct_returns_array,
                                                                hv_array,
                                                                asset_names,
                                                                indicators_and_params,
                                                                vol_adjustement,
                                                                long_bias_adjustment)

    return data_arrays_to_dataframe(raw_adjusted_returns_array, 
                                    dates_index, 
                                    indicators_and_params, 
                                    asset_names)