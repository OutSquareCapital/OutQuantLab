import pandas as pd

def random_fill(series: pd.Series) -> pd.Series:

    nan_indices = series[series.isna()].index

    non_nan_series = series.dropna()

    for idx in nan_indices:
        random_sample = non_nan_series.sample(n=1, replace=True)

        series.at[idx] = random_sample

    return series

def adjust_prices_for_negativity(prices_df: pd.DataFrame) -> pd.DataFrame:

    min_prices = prices_df.min()
    adjustment = abs(min_prices) + (min_prices.abs().max() * 0.01)  
    affected_columns = []

    prices_df = prices_df.apply(lambda col: col + adjustment[col.name] if col.min() <= 0 else col)
    
    for col in prices_df.columns:
        if min_prices[col] <= 0:
            affected_columns.append(col)
    
    if affected_columns:
        print(f"Colonnes affectées par l'ajustement pour prix négatifs: {affected_columns}")
    else:
        print("Aucune colonne affectée par l'ajustement pour prix négatifs")

    return prices_df

def adjust_returns_for_inversion(returns_df: pd.DataFrame, columns_list: list) -> pd.DataFrame:

    for column in columns_list:
        returns = returns_df[column]
        inverted_returns = returns * -1
        inverted_returns_df = inverted_returns.to_frame(name=column)
        returns_df[column] = inverted_returns_df
    
    return returns_df

def adjust_returns_for_nans(returns_df: pd.DataFrame) -> pd.DataFrame:

    for col in returns_df.columns:
        first_valid_index = returns_df[col].first_valid_index()
        if first_valid_index is not None:

            num_days = len(returns_df.loc[first_valid_index:])
            
            num_cells_filled_before = returns_df[col].loc[first_valid_index:].isna().sum()

            returns_df.loc[first_valid_index:, col] = random_fill(returns_df.loc[first_valid_index:, col])

            filled_pct = ((num_cells_filled_before / num_days) * 100).round(2) if num_days > 0 else 0
            absolute_max_returns = returns_df[col].abs().max() * 100
            absolute_median_returns = returns_df[col].abs().median() * 100
            max_returns_date = returns_df[col].idxmax().strftime('%Y-%m-%d')

            print(
                f"Actif : {col}, "
                f"Nombre de cellules aberrantes : {num_cells_filled_before}, "
                f"Proportion d'aberrants: {filled_pct}%, "
                f"Max absolu des rendements : {absolute_max_returns:.2f}% (le {max_returns_date}), "
                f"Médiane absolue des rendements : {absolute_median_returns:.2f}%"
            )

    return returns_df

