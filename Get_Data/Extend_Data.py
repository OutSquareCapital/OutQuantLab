import pandas as pd
import numpy as np

def raccommoder_prices_futures_etf(data_futures_returns_df, data_etf_returns_df, paires_futures_etf):

    raccommodage_dfs = []

    for future, etf in paires_futures_etf:
        if future in data_futures_returns_df.columns and etf in data_etf_returns_df.columns:
            future_returns = data_futures_returns_df[future]
            etf_returns = data_etf_returns_df[etf]

            first_valid_index = future_returns.first_valid_index()

            etf_returns_limited = etf_returns.loc[:first_valid_index]

            first_valid_etf_index = etf_returns_limited.first_valid_index()

            if first_valid_etf_index:
                etf_returns_limited = etf_returns.loc[first_valid_etf_index:first_valid_index]

                combined_returns = future_returns.combine_first(etf_returns_limited)

                print(f"Paire identifiée : {future} et {etf}")

                if not etf_returns_limited.empty:
                    print(f"Plage de rallongement pour {future} et {etf} : {etf_returns_limited.index[0]} à {etf_returns_limited.index[-1]}")

                raccommodage_dfs.append(pd.DataFrame({future: combined_returns}))
            else:
                print(f"Paire ignorée (ETF entièrement NaN avant {first_valid_index}) : {future} et {etf}")

    raccommodage_returns_df = pd.concat(raccommodage_dfs, axis=1)

    final_df = data_futures_returns_df.copy()
    final_df.update(raccommodage_returns_df)
    
    columns_raccommodated = raccommodage_returns_df.columns

    columns_non_raccommodated = data_futures_returns_df.columns.difference(columns_raccommodated)

    for col in columns_non_raccommodated:
        assert final_df[col].equals(data_futures_returns_df[col]), f"Colonne {col} a été modifiée alors qu'elle ne devait pas l'être !"
        
    return final_df

def reconstruct_bond_price_with_yield(yield_10y_df, maturity_years=10, face_value=100):

    return face_value / (1 + yield_10y_df.iloc[:, 0] / 100) ** maturity_years

def adjust_prices_with_risk_free_rate(returns_df, risk_free_rate_df):

    first_price_date = returns_df.index.min()
    print(f"First date in prices_df: {first_price_date}")
    risk_free_rate_df = risk_free_rate_df[risk_free_rate_df.index >= first_price_date]
    print(f"First date in risk_free_rate_df after filtering: {risk_free_rate_df.index.min()}")

    risk_free_rate_aligned = risk_free_rate_df.reindex(returns_df.index, method='ffill')

    missing_dates = returns_df.index.difference(risk_free_rate_df.index)
    if not missing_dates.empty:
        print(f"Dates missing in risk_free_rate_df filled by ffill: {missing_dates}")

    risk_free_daily = (1 + risk_free_rate_aligned.iloc[:, 0] / 100) ** (1 / 252) - 1

    risk_free_daily_expanded = pd.DataFrame(
        np.tile(risk_free_daily.values, (returns_df.shape[1], 1)).T,
        index=returns_df.index,
        columns=returns_df.columns,
        dtype=np.float32
    )

    return returns_df.sub(risk_free_daily_expanded, axis=0)