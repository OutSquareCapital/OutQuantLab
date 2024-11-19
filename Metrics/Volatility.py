import numpy as np
import pandas as pd
import Config
import bottleneck as bn
import numbagg as nb
from Metrics.Aggregation import rolling_mean, rolling_median

def rolling_volatility(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return bn.move_std(array, window=length, min_count=min_length, axis=0, ddof = 1)


def rolling_volatility_(array: np.ndarray, length: int, min_length: int = 1) -> np.ndarray:

    return nb.move_std(array, window=length, min_count=min_length, axis=0)

def hv_short_term_array(returns_array: np.ndarray, lengths_list=[8, 16, 32, 64]) -> np.ndarray:

    hv_arrays = np.array([rolling_volatility(returns_array, length=length, min_length=length)
                            for length in lengths_list])

    return np.nanmean(hv_arrays, axis=0)


def hv_long_term_array(short_term_vol_array: np.ndarray, long_term_lengths=[200, 400, 800, 1600, 3200]) -> np.ndarray:

    long_term_vol_arrays = np.array([rolling_median(short_term_vol_array, length)
                                        for length in long_term_lengths])

    return np.nanmean(long_term_vol_arrays, axis=0)


def hv_composite_array(returns_array: np.ndarray, 
                       lengths=[8, 16, 32, 64], 
                       long_term_lengths=[200, 400, 800, 1600, 3200], 
                       st_weight=0.6, 
                       annualization=True) -> np.ndarray:

    short_term_vol_array = hv_short_term_array(returns_array, lengths_list=lengths)

    # Calculer la volatilité long terme
    long_term_vol_array = hv_long_term_array(short_term_vol_array, long_term_lengths=long_term_lengths)

    # Pondérer court terme et long terme en fonction de st_weight
    lt_weight = 1 - st_weight  # Le poids de la volatilité long terme est l'inverse de st_weight
    composite_vol_array = (st_weight * short_term_vol_array) + (lt_weight * long_term_vol_array)

    if annualization:

        composite_vol_array = composite_vol_array * Config.ANNUALIZED_PERCENTAGE_FACTOR

    return rolling_mean(composite_vol_array, length=5)




def hv_df(returns_df: pd.DataFrame, volatility_length=20) -> pd.DataFrame:

    return returns_df.rolling(window=volatility_length, min_periods=volatility_length).std()


def hv_short_term_df(returns_df: pd.DataFrame, lengths=[8, 16, 32, 64]) -> pd.DataFrame:

    vol_dfs = []
    for length in lengths:
        hv = hv_df(returns_df, volatility_length=length)
        vol_dfs.append(hv)

    return pd.concat(vol_dfs, axis=0).groupby(level=0).mean()


def hv_long_term_df(short_term_vol_df: pd.DataFrame, long_term_lengths=[200, 400, 800, 1600, 3200]) -> pd.DataFrame:

    long_term_vol_dfs = []
    for length in long_term_lengths:
        rolling_median_vol = short_term_vol_df.rolling(window=length, min_periods=1).median()
        long_term_vol_dfs.append(rolling_median_vol)

    return pd.concat(long_term_vol_dfs, axis=0).groupby(level=0).mean()


def hv_composite_df(returns_df: pd.DataFrame, 
                    lengths=[8, 16, 32, 64], 
                    long_term_lengths=[200, 400, 800, 1600, 3200], 
                    st_weight=0.6, 
                    annualization=True) -> pd.DataFrame:

    short_term_vol_df = hv_short_term_df(returns_df, lengths=lengths)

    # Calculer la volatilité long terme
    long_term_vol_df = hv_long_term_df(short_term_vol_df, long_term_lengths=long_term_lengths)

    # Pondérer court terme et long terme en fonction de st_weight
    lt_weight = 1 - st_weight  # Le poids de la volatilité long terme est l'inverse de st_weight

    composite_vol_df = (st_weight * short_term_vol_df) + (lt_weight * long_term_vol_df)

    if annualization:
        composite_vol_df = composite_vol_df * Config.ANNUALIZED_PERCENTAGE_FACTOR

    return composite_vol_df.rolling(window=5, min_periods=1).mean()

def separate_volatility(array:np.ndarray, LenVol: int) -> np.ndarray:

    # Séparation des rendements positifs et négatifs, tout en conservant les NaN
    positive_returns = np.where(np.isnan(array), np.nan, np.where(array > 0, array, 0))
    negative_returns = np.where(np.isnan(array), np.nan, np.where(array < 0, array, 0))

    # Calcul de la volatilité pour les rendements positifs et négatifs
    vol_positive = rolling_volatility(positive_returns, length=LenVol, min_length=1)
    vol_negative = rolling_volatility(negative_returns, length=LenVol, min_length=1)

    return vol_positive, vol_negative

