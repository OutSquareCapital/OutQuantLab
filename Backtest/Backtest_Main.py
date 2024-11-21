import pandas as pd
import numpy as np
from .Backtest_Process import transform_signals_into_returns

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

def process_backtest(prices_array: np.ndarray, 
                    log_returns_array: np.ndarray,
                    volatility_adjusted_pct_returns_array: np.ndarray,
                    asset_names: list,
                    dates_index: pd.Index,
                    indicators_and_params: dict
                    ) -> tuple[pd.DataFrame, pd.DataFrame]:

    raw_adjusted_returns_array = transform_signals_into_returns(prices_array,
                                                                log_returns_array,
                                                                volatility_adjusted_pct_returns_array,
                                                                asset_names,
                                                                indicators_and_params)

    return data_arrays_to_dataframe(raw_adjusted_returns_array, 
                                    dates_index, 
                                    indicators_and_params, 
                                    asset_names)