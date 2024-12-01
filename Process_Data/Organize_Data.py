import pandas as pd
import numpy as np
from typing import List, Dict
import Metrics as mt
import Process_Data.Transform_Data as TransformData

def generate_data_categories(assets_names: List[str], 
                             assets_to_backtest: Dict[str, List[str]]
                             ) -> Dict[str, List[str]]:
    
    # Initialisation des catégories avec des listes vides
    categories = {key: [] for key in assets_to_backtest.keys()}
    
    # Parcourir les assets disponibles et les ajouter dans les catégories correspondantes
    for asset in assets_names:
        for category, assets_list in assets_to_backtest.items():
            if asset in assets_list:
                categories[category].append(asset)

    return categories

def generate_category_dataframes(data_prices_df: pd.DataFrame, 
                                categories: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:

    category_returns_dfs = {}

    returns_df = data_prices_df.pct_change(fill_method=None)

    returns_df = TransformData.adjust_returns_for_inversion(returns_df, ['VIXY'])
    
    # Boucle unique pour traiter toutes les catégories de manière uniforme
    for category, assets_list in categories.items():
        if assets_list:
            # Filtrer les colonnes de data_prices_df correspondant aux actifs de la catégorie
            category_returns_dfs[category] = returns_df[assets_list]
        else:
            # Générer un DataFrame vide si la liste est vide
            category_returns_dfs[category] = pd.DataFrame(dtype=np.float32)

    return category_returns_dfs

def calculate_all_ensembles_and_ratios(category_returns_dfs: dict) -> dict:

    category_ratios_ensembles_returns_df = {}

    for category_name, returns_df in category_returns_dfs.items():

        if not returns_df.empty:

            asset_names = returns_df.columns.tolist()

            if category_name in ['assets', 'canary_assets']:
                # Renvoie simplement les rendements pour 'assets' et 'canary_assets'
                category_ratios_ensembles_returns_df[category_name] = returns_df

            elif category_name in ['ratios', 'canary_ratios', 'ensembles', 'canary_ensembles']:
                
                hv = pd.DataFrame(mt.hv_composite(returns_df.values), 
                                  index=returns_df.index, 
                                  columns=returns_df.columns, 
                                  dtype=np.float32)

                adjusted_returns_df = pd.DataFrame(TransformData.calculate_volatility_adjusted_returns(returns_df.values, hv), 
                                                   index=returns_df.index, 
                                                   columns=returns_df.columns,
                                                   dtype=np.float32)

                if category_name in ['ensembles', 'canary_ensembles']:
                    # Générer les ensembles à partir des rendements ajustés
                    ensembles_returns_df = TransformData.calculate_ensembles_returns(adjusted_returns_df, asset_names)

                    # Renvoie directement les rendements des ensembles
                    category_ratios_ensembles_returns_df[category_name] = ensembles_returns_df

                elif category_name in ['ratios', 'canary_ratios']:
                    # Générer les ratios à partir des rendements ajustés
                    ratios_returns_df = TransformData.calculate_ratios_returns(adjusted_returns_df, asset_names)

                    # Renvoie directement les rendements des ratios
                    category_ratios_ensembles_returns_df[category_name] = ratios_returns_df

        else:
            # Si le DataFrame est vide, on le laisse vide
            category_ratios_ensembles_returns_df[category_name] = pd.DataFrame(dtype=np.float32)

    return category_ratios_ensembles_returns_df

def recombine_categories(category_returns_dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:

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

def extract_category_data(category_dfs: Dict[str, pd.DataFrame]):
    # Un dictionnaire pour stocker les résultats pour chaque catégorie
    category_extracted_data = {}

    for category, df in category_dfs.items():
        if not df.empty:  # Si le DataFrame n'est pas vide
            # Appliquer extract_data_from_prices pour chaque DataFrame non vide
            (
                prices_array,
                volatility_adjusted_pct_returns,
                log_returns_array,
                asset_names,
                dates_index
            ) = TransformData.extract_data_from_pct_returns(df)

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
                        assets_names: List[str], 
                        data_prices_df: pd.DataFrame, 
                        assets_to_backtest: Dict[str, List[str]]
                        ) -> Dict[str, Dict[str, any]]:

    # Génération du dictionnaire des catégories
    categories = generate_data_categories(assets_names, assets_to_backtest)

    # Génération des DataFrames de returns pour chaque catégorie
    base_category_returns_dfs = generate_category_dataframes(data_prices_df, categories)

    # Calcul de tous les ensembles et ratios
    all_category_returns_dfs = calculate_all_ensembles_and_ratios(base_category_returns_dfs)

    # Recombiner les catégories en 'returnstreams' et 'canary_all'
    recombined_category_returns_dfs = recombine_categories(all_category_returns_dfs)

    return extract_category_data(recombined_category_returns_dfs)

def process_data(assets_names: List[str], 
                data_prices_df: pd.DataFrame, 
                assets_to_backtest: Dict[str, List[str]]
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