import pandas as pd
import numpy as np
from scipy.stats import skew
import Config
from Process_Data import equity_curves_calculs
import Metrics as mt

def overall_sharpe_ratios_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    sharpe_ratios = daily_returns.mean() / daily_returns.std() * Config.ANNUALIZATION_FACTOR

    return pd.DataFrame(sharpe_ratios, 
                        columns=['Sharpe Ratio'], 
                        dtype=np.float32
                        ).round(2)

def overall_sortino_ratios_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    mean_returns = daily_returns.mean()
    
    downside_deviation = daily_returns[daily_returns < 0].std()
    
    sortino_ratios = mean_returns / downside_deviation * Config.ANNUALIZATION_FACTOR

    return pd.DataFrame(sortino_ratios, 
                        columns=['Sortino Ratio'], 
                        dtype=np.float32
                        ).round(2)

def rolling_sharpe_ratios_calculs(daily_returns: pd.DataFrame, window_size: int = 1250):
        
        return pd.DataFrame(mt.rolling_sharpe_ratios(
                                                    daily_returns.values, 
                                                    window_size, 
                                                    window_size),
                                                    index=daily_returns.index,
                                                    columns=daily_returns.columns
                                                    ).round(2)
        

def rolling_volatility_calculs(daily_returns: pd.DataFrame, means):
    
    if means:
        rolling_volatility_df = pd.DataFrame(mt.hv_composite(daily_returns.values), 
                                             index=daily_returns.index, 
                                             columns=daily_returns.columns)
        return rolling_volatility_df.expanding(min_periods=1).mean().round(2)
    else:
        return pd.DataFrame(mt.hv_composite(daily_returns.values), 
                                             index=daily_returns.index, 
                                             columns=daily_returns.columns).round(2)

def calculate_final_equity_values(daily_returns: pd.DataFrame, initial_equity: int = 100000) -> pd.DataFrame:

    final_equities = []
    for start_date in daily_returns.index:
        # Calculer les courbes d'équité en utilisant cumprod depuis le start_date
        equity_curve = (1 + daily_returns.loc[start_date:]).cumprod() * initial_equity
        final_values = equity_curve.iloc[-1]
        final_equities.append(final_values)

    return pd.DataFrame(final_equities, 
                                        index=daily_returns.index, 
                                        columns=daily_returns.columns, 
                                        dtype=np.float32).round(2)

def drawdowns_calculs(returns_df: pd.DataFrame) -> pd.DataFrame:

    equity_curves = equity_curves_calculs(returns_df)
    
    # Calculate drawdowns for each equity curve directly
    drawdowns = (equity_curves - equity_curves.cummax()) / equity_curves.cummax() * Config.PERCENTAGE_FACTOR

    return drawdowns.round(2)

def annual_returns_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    # Grouper les rendements par année
    grouped = daily_returns.groupby(daily_returns.index.year)

    # Calculer les rendements cumulés pour chaque groupe (année)
    cumulative_returns = grouped.apply(lambda x: (x + 1).prod() - 1) * Config.PERCENTAGE_FACTOR

    return pd.DataFrame(cumulative_returns, 
                        dtype=np.float32
                        ).round(4)

def average_correlation_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    correlation_matrix = daily_returns.corr()
    average_correlations = correlation_matrix.mean()

    return pd.DataFrame(average_correlations, 
                        columns=['Average Correlation'], 
                        dtype=np.float32
                        ).round(2)

def calculate_sharpe_correlation_ratio(daily_returns: pd.DataFrame) -> pd.DataFrame:

    # Calcul des Sharpe Ratios et des Average Correlations
    sharpe_ratios_df = overall_sharpe_ratios_calculs(daily_returns)
    average_correlations_df = average_correlation_calculs(daily_returns)

    # Calculer les rangs des Sharpe Ratios et des Correlations indépendamment
    sharpe_ratios_df['Sharpe Rank'] = sharpe_ratios_df['Sharpe Ratio'].rank(method='min')
    average_correlations_df['Correlation Rank'] = average_correlations_df['Average Correlation'].rank(method='min')

    # Fusionner les deux DataFrames avec pd.concat en s'assurant que les index sont alignés
    combined_df = pd.concat([sharpe_ratios_df, average_correlations_df], axis=1)

    # Calculer la nouvelle métrique : Sharpe Rank / Correlation Rank
    combined_df['Sharpe/AvgCorrelation'] = combined_df['Sharpe Rank'] / combined_df['Correlation Rank']

    return combined_df

def sharpe_ratios_yearly_calculs(daily_returns: pd.DataFrame) -> pd.DataFrame:

    # Grouper les retours par année
    grouped = daily_returns.groupby(daily_returns.index.year)

    # Calculer les ratios de Sharpe pour chaque groupe (année)
    sharpe_ratios = grouped.apply(lambda x: sharpe_ratios_yearly_calculs(x)['Sharpe Ratio'])

    return pd.DataFrame(sharpe_ratios, dtype=np.float32)

def overall_monthly_skew_calculs(returns_df: pd.DataFrame) -> pd.Series:

    # Agréger par mois pour obtenir les rendements mensuels moyens pour chaque actif
    monthly_returns_df = returns_df.resample('ME').mean()
    
    return monthly_returns_df.apply(lambda x: skew(x, nan_policy='omit')
                                    ).astype(np.float32
                                    ).round(2)
                        