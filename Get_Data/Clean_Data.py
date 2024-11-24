import pandas as pd

def random_fill(series: pd.Series) -> pd.Series:

    nan_indices = series[series.isna()].index

    non_nan_series = series.dropna()

    # Boucle sur chaque NaN pour le remplacer par un rendement aléatoire du même actif
    for idx in nan_indices:
        # Tirer X samples aléatoires parmi les rendements non NaN
        random_sample = non_nan_series.sample(n=1, replace=True)

        # Remplacer le NaN par la valeur échantillonnée
        series.at[idx] = random_sample

    return series

def adjust_prices_for_negativity(prices_df: pd.DataFrame) -> pd.DataFrame:

    # Ajuster les séries de prix pour qu'aucune valeur ne soit négative
    min_prices = prices_df.min()
    adjustment = abs(min_prices) + (min_prices.abs().max() * 0.01)  # Ajustement basé sur 1% du min absolu max
    # Liste pour suivre les colonnes ajustées
    affected_columns = []

    # Appliquer l'ajustement et suivre les colonnes affectées
    prices_df = prices_df.apply(lambda col: col + adjustment[col.name] if col.min() <= 0 else col)
    
    # Identifier les colonnes affectées
    for col in prices_df.columns:
        if min_prices[col] <= 0:
            affected_columns.append(col)
    
    # Imprimer les colonnes affectées
    if affected_columns:
        print(f"Colonnes affectées par l'ajustement pour prix négatifs: {affected_columns}")
    else:
        print("Aucune colonne affectée par l'ajustement pour prix négatifs")

    return prices_df

def adjust_returns_for_nans(returns_df: pd.DataFrame) -> pd.DataFrame:

    for col in returns_df.columns:
        first_valid_index = returns_df[col].first_valid_index()
        if first_valid_index is not None:

            # Calculer le nombre de jours (différence entre le premier prix valide et la fin des données)
            num_days = len(returns_df.loc[first_valid_index:])
            
            # Avant de faire le ffill, compter les NaNs après le premier prix valide
            num_cells_filled_before = returns_df[col].loc[first_valid_index:].isna().sum()

            # Appliquer le bootstrap pour remplir les NaNs après le premier jour valide
            returns_df.loc[first_valid_index:, col] = random_fill(returns_df.loc[first_valid_index:, col])

            # Calculer les statistiques
            filled_pct = ((num_cells_filled_before / num_days) * 100).round(2) if num_days > 0 else 0
            absolute_max_returns = returns_df[col].abs().max() * 100
            absolute_median_returns = returns_df[col].abs().median() * 100
            # Trouver les dates associées au max des rendements
            max_returns_date = returns_df[col].idxmax().strftime('%Y-%m-%d')

            # Imprimer les statistiques
            print(
                f"Actif : {col}, "
                f"Nombre de cellules aberrantes : {num_cells_filled_before}, "
                f"Proportion d'aberrants: {filled_pct}%, "
                f"Max absolu des rendements : {absolute_max_returns:.2f}% (le {max_returns_date}), "
                f"Médiane absolue des rendements : {absolute_median_returns:.2f}%"
            )

    return returns_df

