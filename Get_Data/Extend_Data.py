import pandas as pd
import numpy as np

def raccommoder_prices_futures_etf(data_futures_df, data_etf_df, paires_futures_etf):
    """
    Fonction qui remplace les prix manquants des futures par les ETF correspondants en utilisant les rendements
    en pourcentage, jusqu'au premier index valide des futures. Ensuite, les prix sont reconstruits à partir de 100.
    Les colonnes des futures qui ont été raccommodées sont remplacées dans le DataFrame final.

    Args:
    - data_futures_df (pd.DataFrame): DataFrame contenant les prix des futures avec un index de dates.
    - data_etf_df (pd.DataFrame): DataFrame contenant les prix des ETF avec un index de dates.
    - paires_futures_etf (list of tuples): Liste de tuples avec les paires futures/ETF sous la forme [(future1, etf1), (future2, etf2), ...]

    Returns:
    - pd.DataFrame: DataFrame finale avec les prix raccommodés à partir des rendements des ETF et futures, reconstitués avec cumprod.
    """
    raccommodage_dfs = []

    # Calcul des rendements (pct change) pour les futures et ETF
    data_futures_returns_df = data_futures_df.pct_change()
    data_etf_returns_df = data_etf_df.pct_change()

    # Parcourir les paires fournies (futures et ETF)
    for future, etf in paires_futures_etf:
        if future in data_futures_returns_df.columns and etf in data_etf_returns_df.columns:
            future_returns = data_futures_returns_df[future]
            etf_returns = data_etf_returns_df[etf]

            # Trouver le premier index valide du future
            first_valid_index = future_returns.first_valid_index()

            # Limiter les rendements de l'ETF jusqu'à ce premier index
            etf_returns_limited = etf_returns.loc[:first_valid_index]

            # Trouver la première date non-NaN dans les rendements de l'ETF avant le first_valid_index du future
            first_valid_etf_index = etf_returns_limited.first_valid_index()

            if first_valid_etf_index:
                # Limiter les rendements de l'ETF à partir de la première date non-NaN de l'ETF
                etf_returns_limited = etf_returns.loc[first_valid_etf_index:first_valid_index]

                # Fusionner les rendements des futures avec ceux de l'ETF à partir de cette date
                combined_returns = future_returns.combine_first(etf_returns_limited)

                # Ajouter la paire identifiée
                print(f"Paire identifiée : {future} et {etf}")

                # Si des dates de l'ETF ont été utilisées pour rallonger les futures
                if not etf_returns_limited.empty:
                    print(f"Plage de rallongement pour {future} et {etf} : {etf_returns_limited.index[0]} à {etf_returns_limited.index[-1]}")

                # Conserver le résultat dans une nouvelle DataFrame
                raccommodage_dfs.append(pd.DataFrame({future: combined_returns}))
            else:
                print(f"Paire ignorée (ETF entièrement NaN avant {first_valid_index}) : {future} et {etf}")

    # Concaténer toutes les colonnes raccommodées (rendements)
    raccommodage_returns_df = pd.concat(raccommodage_dfs, axis=1)

    # Reconstituer les prix en utilisant cumprod() en partant de 100 pour les colonnes raccommodées
    raccommodage_prices_df = (1 + raccommodage_returns_df).cumprod() * 100

    # Remplacer les colonnes raccommodées dans le DataFrame des futures
    final_df = data_futures_df.copy()  # Copie du DataFrame d'origine
    final_df.update(raccommodage_prices_df)  # Remplacer uniquement les colonnes raccommodées
    
    # Vérification que les colonnes non mises à jour sont identiques entre final_df et data_futures_df
    columns_raccommodated = raccommodage_prices_df.columns  # Colonnes qui ont été raccommodées

    # Identifier les colonnes qui n'ont pas été raccommodées
    columns_non_raccommodated = data_futures_df.columns.difference(columns_raccommodated)

    # Vérifier que les dates, valeurs et NaN des colonnes non modifiées sont identiques
    for col in columns_non_raccommodated:
        assert final_df[col].equals(data_futures_df[col]), f"Colonne {col} a été modifiée alors qu'elle ne devait pas l'être !"
        
    return final_df


def reconstruct_bond_price_with_yield(yield_10y_df, maturity_years=10, face_value=100):
    """
    Fonction qui simule le prix d'une obligation à maturité constante à partir des taux d'intérêt quotidiens (annualisés).
    Utilise la formule classique de l'obligation en actualisant les coupons et la valeur nominale.
    Ne prends pas en compte le versement de dividendes!!
    Args:
    - yield_10y_df (pd.DataFrame): DataFrame contenant les taux d'intérêt quotidiens (annualisés) avec un index de dates.
    - maturity_years (float): Durée de vie constante de l'obligation en années (par défaut 10 ans).
    - face_value (float): Valeur nominale de l'obligation (par défaut 100).

    Returns:
    - pd.DataFrame: DataFrame contenant les prix reconstitués de l'obligation.
    """

    
    # 2. Pour chaque jour, calculer le prix de l'obligation en utilisant la formule classique
    bond_price_df = face_value / (1 + yield_10y_df.iloc[:, 0] / 100) ** maturity_years

    return bond_price_df

def adjust_prices_with_risk_free_rate(prices_df, risk_free_rate_df):
    """
    Fonction qui ajuste les prix des actifs en utilisant les taux d'intérêt sans risque (par ex. US 3M)
    pour simuler la détention de contrats futures. Les rendements des actifs sont ajustés quotidiennement
    en soustrayant leur rendement du rendement sans risque.

    Args:
    - prices_df (pd.DataFrame): DataFrame contenant les prix des actifs avec un index de dates.
    - risk_free_rate_df (pd.DataFrame): DataFrame contenant les valeurs absolues des taux d'intérêt sans risque (annualisés) à une colonne.

    Returns:
    - pd.DataFrame: DataFrame contenant les prix ajustés des actifs.
    """

    # 1. Filtrer les lignes de risk_free_rate_df dont les dates sont antérieures à la première date de prices_df
    first_price_date = prices_df.index.min()
    print(f"First date in prices_df: {first_price_date}")
    risk_free_rate_df = risk_free_rate_df[risk_free_rate_df.index >= first_price_date]
    print(f"First date in risk_free_rate_df after filtering: {risk_free_rate_df.index.min()}")

    # 2. Aligner les taux sans risque avec les dates des actifs, avec reindex et ffill pour les valeurs manquantes
    risk_free_rate_aligned = risk_free_rate_df.reindex(prices_df.index, method='ffill')

    # 3. Imprimer les dates où ffill a été appliqué
    missing_dates = prices_df.index.difference(risk_free_rate_df.index)
    if not missing_dates.empty:
        print(f"Dates missing in risk_free_rate_df filled by ffill: {missing_dates}")

    # 4. Calculer les rendements quotidiens des taux sans risque
    risk_free_daily = (1 + risk_free_rate_aligned.iloc[:, 0] / 100) ** (1 / 252) - 1

    # 5. Calcul des rendements quotidiens des actifs
    returns_df = prices_df.pct_change()

    # 6. Étendre les rendements quotidiens du taux sans risque à toutes les colonnes des actifs
    risk_free_daily_expanded = pd.DataFrame(
        np.tile(risk_free_daily.values, (returns_df.shape[1], 1)).T,
        index=returns_df.index,
        columns=returns_df.columns,
        dtype=np.float32
    )

    # 7. Soustraire les rendements des actifs des rendements journaliers du taux sans risque
    adjusted_returns_df = returns_df.sub(risk_free_daily_expanded, axis=0)

    # 8. Reconstituer les prix ajustés à partir des rendements ajustés
    adjusted_prices_df = (1 + adjusted_returns_df).cumprod() * 100  # On part d'une base de 100

    return adjusted_prices_df