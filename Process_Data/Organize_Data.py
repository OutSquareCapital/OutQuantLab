import pandas as pd
import numpy as np
import Metrics as mt
from .Transform_Data import (equity_curves_calculs, 
                            log_returns_np, 
                            adjust_returns_for_inversion, 
                            calculate_volatility_adjusted_returns, 
                            calculate_ensembles_returns, 
                            extract_data_from_pct_returns, 
                            calculate_ratios_returns
                            )
from typing import Any

def generate_data_categories(assets_names: list[str], 
                             assets_to_backtest: dict[str, list[str]]
                             ) -> dict[str, list[str]]:
    
    categories = {key: [] for key in assets_to_backtest.keys()}
    
    for asset in assets_names:
        for category, assets_list in assets_to_backtest.items():
            if asset in assets_list:
                categories[category].append(asset)

    return categories

def generate_category_dataframes(data_prices_df: pd.DataFrame, 
                                categories: dict[str, list[str]]) -> dict[str, pd.DataFrame]:

    category_returns_dfs: dict[str, pd.DataFrame] = {}

    returns_df = data_prices_df.pct_change(fill_method=None)

    returns_df = adjust_returns_for_inversion(returns_df, ['VIXY'])
    
    for category, assets_list in categories.items():
        if assets_list:
            category_returns_dfs[category] = returns_df[assets_list]
        else:
            category_returns_dfs[category] = pd.DataFrame(dtype=np.float32)

    return category_returns_dfs

def calculate_all_ensembles_and_ratios(category_returns_dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:

    category_ratios_ensembles_returns_df: dict[str, pd.DataFrame] = {}

    for category_name, returns_df in category_returns_dfs.items():

        if not returns_df.empty:

            asset_names = returns_df.columns.tolist()

            if category_name in ['assets', 'canary_assets']:
                category_ratios_ensembles_returns_df[category_name] = returns_df

            elif category_name in ['ratios', 'canary_ratios', 'ensembles', 'canary_ensembles']:
                
                hv = mt.hv_composite(returns_df.values)

                adjusted_returns_df = pd.DataFrame(calculate_volatility_adjusted_returns(returns_df.values, hv), 
                                                   index=returns_df.index, 
                                                   columns=returns_df.columns,
                                                   dtype=np.float32)

                if category_name in ['ensembles', 'canary_ensembles']:
                    ensembles_returns_df = calculate_ensembles_returns(adjusted_returns_df, asset_names)
                    category_ratios_ensembles_returns_df[category_name] = ensembles_returns_df

                elif category_name in ['ratios', 'canary_ratios']:
                    ratios_returns_df = calculate_ratios_returns(adjusted_returns_df, asset_names)
                    category_ratios_ensembles_returns_df[category_name] = ratios_returns_df

        else:
            category_ratios_ensembles_returns_df[category_name] = pd.DataFrame(dtype=np.float32)

    return category_ratios_ensembles_returns_df

def recombine_categories(category_returns_dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:

    combined_category_dfs = {}

    # Combiner les catégories pour 'returnstreams'
    returnstreams_categories = ['assets', 'ratios', 'ensembles']
    combined_returnstreams_df = pd.concat([category_returns_dfs[cat] for cat in returnstreams_categories if not category_returns_dfs[cat].empty], axis=1)
    combined_category_dfs['returnstreams'] = combined_returnstreams_df

    # Combiner les catégories pour 'canary_all'
    canary_categories = ['canary_assets', 'canary_ratios', 'canary_ensembles']
    
    # Vérifier s'il y a des catégories non vides dans canary
    canary_dataframes = [category_returns_dfs[cat] for cat in canary_categories if not category_returns_dfs[cat].empty]
    if canary_dataframes:
        # Si au moins une catégorie canary est non vide, on les concatène
        combined_canary_all_df = pd.concat(canary_dataframes, axis=1)
        combined_category_dfs['canary_all'] = combined_canary_all_df
    else:
        # Sinon, on crée un DataFrame vide pour 'canary_all'
        combined_category_dfs['canary_all'] = pd.DataFrame(dtype=np.float32)
    return combined_category_dfs

def extract_category_data(category_dfs: dict[str, pd.DataFrame]) -> dict[str, Any]:
    category_extracted_data = {}

    for category, df in category_dfs.items():
        if not df.empty:
            (
                prices_array,
                volatility_adjusted_pct_returns,
                log_returns_array,
                asset_names,
                dates_index
            ) = extract_data_from_pct_returns(df)

            # Stocker les résultats dans le dictionnaire
            category_extracted_data[category] = {
                'prices_array': prices_array,
                'volatility_adjusted_pct_returns': volatility_adjusted_pct_returns,
                'log_returns_array': log_returns_array,
                'asset_names': asset_names,
                'dates': dates_index
            }

    return category_extracted_data

def process_category_data(
                        assets_names: list[str], 
                        data_prices_df: pd.DataFrame, 
                        assets_to_backtest: dict[str, list[str]]
                        ) -> dict[str, dict[str, Any]]:

    # Génération du dictionnaire des catégories
    categories = generate_data_categories(assets_names, assets_to_backtest)

    # Génération des DataFrames de returns pour chaque catégorie
    base_category_returns_dfs = generate_category_dataframes(data_prices_df, categories)

    # Calcul de tous les ensembles et ratios
    all_category_returns_dfs = calculate_all_ensembles_and_ratios(base_category_returns_dfs)

    # Recombiner les catégories en 'returnstreams' et 'canary_all'
    recombined_category_returns_dfs = recombine_categories(all_category_returns_dfs)

    return extract_category_data(recombined_category_returns_dfs)

def process_data_old(assets_names: list[str], 
                data_prices_df: pd.DataFrame, 
                assets_to_backtest: dict[str, list[str]]
                ):

    data = process_category_data(assets_names,
                                data_prices_df, 
                                assets_to_backtest)   

    prices_array = data['returnstreams']['prices_array']
    volatility_adjusted_pct_returns_array = data['returnstreams']['volatility_adjusted_pct_returns']
    log_returns_array = data['returnstreams']['log_returns_array']
    asset_names = data['returnstreams']['asset_names']
    dates_index = data['returnstreams']['dates']

    return prices_array, volatility_adjusted_pct_returns_array, log_returns_array, asset_names, dates_index

def process_data(
    data_prices_df: pd.DataFrame
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], pd.Index]:
    
    returns_df=data_prices_df.pct_change(fill_method=None)

    # Calcul des rendements simples
    pct_returns_array = returns_df.to_numpy(dtype=np.float32)

    # Calcul des prix à partir des rendements (cumul des rendements)
    prices_array = equity_curves_calculs(pct_returns_array)

    # Calcul des rendements log
    log_returns_array = log_returns_np(prices_array)

    # Calcul de la volatilité ajustée
    hv_array = mt.hv_composite(pct_returns_array)
    volatility_adjusted_pct_returns = calculate_volatility_adjusted_returns(
        pct_returns_array, hv_array
    )

    # Extraction des noms d'actifs et des dates
    asset_names = list(data_prices_df.columns)
    dates_index = data_prices_df.index

    return prices_array, volatility_adjusted_pct_returns, log_returns_array, asset_names, dates_index
