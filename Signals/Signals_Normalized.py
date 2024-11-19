import numpy as np
from numba import njit
import bottleneck as bn
from Signals.Signals_Raw import *
import Metrics as mt
from Infrastructure import Fast_Tools as ft
import Signals.Signals_Normalization as sn


class Trend :

    @staticmethod
    def mean_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

        mean_price_ratio_raw = RawTrend.calculate_mean_price_ratio_raw(prices_array, LenST, LenLT)
        
        return sn.sign_normalization(mean_price_ratio_raw)

    @staticmethod
    def median_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:
        
        median_price_ratio_raw = RawTrend.calculate_median_price_ratio_raw(prices_array, LenST, LenLT)

        return sn.sign_normalization(median_price_ratio_raw)
        
    
    @staticmethod
    def central_price_ratio(prices_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

        central_price_ratio_raw = RawTrend.calculate_central_price_ratio_raw(prices_array, LenST, LenLT)

        return sn.sign_normalization(central_price_ratio_raw)

    @staticmethod
    def mean_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

        mean_roc_raw = RawTrend.calculate_mean_rate_of_change_raw(returns_array, LenST, LenLT)
        
        return sn.sign_normalization(mean_roc_raw)

    @staticmethod
    def median_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

        median_roc_raw = RawTrend.calculate_median_rate_of_change_raw(returns_array, LenST, LenLT)

        return sn.sign_normalization(median_roc_raw)
    

    @staticmethod
    def central_rate_of_change(returns_array: np.ndarray, LenST: int, LenLT: int) -> np.ndarray:

        central_roc_raw = RawTrend.calculate_central_rate_of_change_raw(returns_array, LenST, LenLT)

        return sn.sign_normalization(central_roc_raw)

class Acceleration :
    
    @staticmethod
    def mean_price_macd(prices_array: np.ndarray, LenST: int, LenLT: int, MacdLength: int) -> np.ndarray:

        mean_price_ratio_macd_raw = RawAcceleration.calculate_mean_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(mean_price_ratio_macd_raw)
    
    @staticmethod
    def median_price_macd(prices_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

        median_price_ratio_macd_raw = RawAcceleration.calculate_median_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(median_price_ratio_macd_raw)

    @staticmethod
    def central_price_macd(prices_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

        central_price_ratio_macd_raw = RawAcceleration.calculate_central_price_macd_raw(prices_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(central_price_ratio_macd_raw)

    @staticmethod
    def mean_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

        mean_roc_macd_raw = RawAcceleration.calculate_mean_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(mean_roc_macd_raw)

    @staticmethod
    def median_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

        median_roc_macd_raw = RawAcceleration.calculate_median_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(median_roc_macd_raw)

    @staticmethod
    def central_rate_of_change_macd(returns_array:np.ndarray, LenST:int, LenLT:int, MacdLength:int) -> np.ndarray:

        central_roc_macd_raw = RawAcceleration.calculate_central_rate_of_change_macd_raw(returns_array, LenST, LenLT, MacdLength)

        return sn.sign_normalization(central_roc_macd_raw)
    
class AccelerationTrend:

    @staticmethod
    def mean_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        mean_price_ratio_signal = Trend.mean_price_ratio(prices_array, TrendLenST, TrendLenLT)

        mean_price_macd_signal =  Acceleration.mean_price_macd(prices_array, LenST, LenLT, MacdLength)

        return sn.calculate_indicator_on_trend_signal(mean_price_ratio_signal, mean_price_macd_signal)

    @staticmethod
    def median_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        median_price_ratio_signal = Trend.median_price_ratio(prices_array, TrendLenST, TrendLenLT)

        median_price_macd_signal = Acceleration.median_price_macd(prices_array, LenST, LenLT, MacdLength)
        
        return sn.calculate_indicator_on_trend_signal(median_price_ratio_signal, median_price_macd_signal)
    
    @staticmethod
    def central_price_macd_trend(prices_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        central_price_ratio_signal = Trend.central_price_ratio(prices_array, TrendLenST, TrendLenLT)

        central_price_macd_signal = Acceleration.central_price_macd(prices_array, LenST, LenLT, MacdLength)

        return sn.calculate_indicator_on_trend_signal(central_price_ratio_signal, central_price_macd_signal)

    @staticmethod
    def mean_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        mean_roc_trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        mean_roc_macd_signal = Acceleration.mean_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
        
        return sn.calculate_indicator_on_trend_signal(mean_roc_trend_signal, mean_roc_macd_signal)

    @staticmethod
    def median_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        median_roc_trend_signal = Trend.median_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        median_roc_macd_signal = Acceleration.median_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)

        return sn.calculate_indicator_on_trend_signal(median_roc_trend_signal, median_roc_macd_signal)

    @staticmethod
    def central_rate_of_change_macd_trend(returns_array:np.ndarray, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:
    
        central_roc_trend_signal = Trend.central_rate_of_change(returns_array, TrendLenST, TrendLenLT)
        
        central_roc_macd_signal = Acceleration.central_rate_of_change_macd(returns_array, LenST, LenLT, MacdLength)
        
        return sn.calculate_indicator_on_trend_signal(central_roc_trend_signal, central_roc_macd_signal)

class RiskPremium:

    @staticmethod
    def fixed_bias(prices_array:np.ndarray, Bias:int) -> np.ndarray:

        return np.full_like(prices_array, Bias, dtype=np.float32)
    
class MeanReversion:

    @staticmethod
    def mean_price_ratio_normalised(prices_array:np.ndarray, SignalLength: int, PLength: int) -> np.ndarray:

        mean_price_ratio = RawTrend.calculate_mean_price_ratio_raw(prices_array, 1, SignalLength)

        return sn.rolling_median_normalisation(-mean_price_ratio, PLength)

    @staticmethod
    def mean_rate_of_change_normalised(returns_array:np.ndarray, SignalLength: int, PLength: int) -> np.ndarray:

        mean_roc = RawTrend.calculate_mean_rate_of_change_raw(returns_array, 1, SignalLength)

        return sn.rolling_median_normalisation(-mean_roc, PLength)

class MeanReversionTrend:

    @staticmethod
    def mean_price_ratio_normalised_trend(prices_array: np.ndarray, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> np.ndarray:

        mean_reversion_signal = MeanReversion.mean_price_ratio_normalised(prices_array, SignalLength, PLength)

        trend_signal = Trend.mean_price_ratio(prices_array, LenST, LenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)

    @staticmethod
    def mean_rate_of_change_normalised_trend(returns_array: np.ndarray, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> np.ndarray:

        mean_reversion_signal = MeanReversion.mean_rate_of_change_normalised(returns_array, SignalLength, PLength)

        trend_signal = Trend.mean_rate_of_change(returns_array, LenST, LenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal) 
    
class SeasonalBreakout:

    @staticmethod
    def seasonal_breakout_returns(prices_array: np.ndarray, LengthMean: int, LengthSnapshot: int, amplitude: int)-> np.ndarray:
        
        # Capture les snapshots à des intervalles réguliers
        repeated_snapshots_array = ft.snapshot_at_intervals(prices_array, LengthSnapshot)

        # Calcul des rendements par rapport aux snapshots
        returns = (prices_array / repeated_snapshots_array) - 1

        abs_returns_array = abs(returns)

        avg_move = SeasonalBreakout.calculate_avg_move_nan(abs_returns_array, LengthSnapshot, LengthMean)

        amplitude_float = np.float32(amplitude)
        amplitude_adjustement = np.float32(10)

        adjusted_amplitude = amplitude_float / amplitude_adjustement

        # Définition des bornes basées sur la moyenne glissante
        upper_bound = avg_move * adjusted_amplitude
        lower_bound = -avg_move * adjusted_amplitude

        signals = np.where(np.isnan(returns) | np.isnan(upper_bound) | np.isnan(lower_bound), np.nan,  # Si l'un des trois est NaN, signal est NaN
                        np.where(returns > upper_bound, 1,  # Si returns > upper_bound, signal est 1 (achat)
                                    np.where(returns < lower_bound, -1, 0)))  # Si returns < lower_bound, signal est -1 (vente), sinon 0
        
        # Forcer le tableau signals en float32
        signals = signals.astype(np.float32)

        return signals*-1

    @njit
    def calculate_avg_move_nan(abs_returns_np: np.ndarray, LengthSnapshot:int, LengthMean:int):
        """
        Calculer la moyenne des mouvements absolus des rendements en excluant les NaN
        sur une fenêtre de temps basée sur LengthPeriod et LengthMean.

        Args:
            abs_returns_np (np.ndarray): Un tableau 2D de rendements absolus (chaque colonne représente un actif).
            LengthPeriod (int): La période entre chaque snapshot (prise de vue) dans l'historique.
            LengthMean (int): Le nombre de snapshots à inclure dans le calcul de la moyenne.

        Returns:
            np.ndarray: Un tableau 2D où chaque cellule contient la moyenne des rendements sur la fenêtre, ou NaN si aucune donnée n'est disponible.
        """
        
        # Obtenir les dimensions du tableau de rendements : num_days est le nombre de lignes (jours), num_assets le nombre d'actifs (colonnes)
        num_days, num_assets = abs_returns_np.shape

        # Créer un tableau vide pour stocker les moyennes calculées pour chaque jour et chaque actif
        avg_move = np.empty((num_days, num_assets), dtype=np.float32)

        # Boucle sur chaque jour i (chaque ligne)
        for i in range(num_days):
            # Générer les indices des snapshots à utiliser pour le calcul de la moyenne
            # Commence à i, puis recule de LengthPeriod à chaque étape, et ne conserve que les LengthMean premiers indices
            snapshot_indices = np.arange(i, -1, -LengthSnapshot)[:LengthMean]

            # Initialiser les variables pour stocker la somme des rendements et le nombre de valeurs valides (non-NaN) pour chaque actif
            total_sum = np.zeros(num_assets, dtype=np.float32)  # Tableau pour accumuler les sommes de rendements par actif
            valid_count = np.zeros(num_assets, dtype=np.float32)  # Compteur du nombre de valeurs valides (non-NaN) par actif

            # Boucle sur les indices des snapshots sélectionnés
            for idx in snapshot_indices:
                # Extraire les rendements pour chaque actif à l'index donné (snapshot)
                values = abs_returns_np[idx]

                # Pour chaque actif, vérifier s'il s'agit d'une valeur valide (non-NaN)
                for asset_idx in range(num_assets):
                    if not np.isnan(values[asset_idx]):  # Si la valeur n'est pas NaN, l'inclure dans le calcul
                        total_sum[asset_idx] += values[asset_idx]  # Ajouter la valeur à la somme courante pour cet actif
                        valid_count[asset_idx] += 1  # Incrémenter le compteur de valeurs valides pour cet actif

            # Calculer la moyenne des rendements pour chaque actif, seulement si des valeurs valides ont été trouvées
            for asset_idx in range(num_assets):
                if valid_count[asset_idx] > 0:
                    # Diviser la somme totale par le nombre de valeurs valides pour obtenir la moyenne
                    avg_move[i, asset_idx] = total_sum[asset_idx] / valid_count[asset_idx]
                else:
                    # Si aucune valeur valide n'a été trouvée, renvoyer NaN pour cet actif
                    avg_move[i, asset_idx] = np.nan

        # Retourner le tableau des moyennes calculées (ou NaN si aucune donnée valide)
        return avg_move

class SeasonalBreakoutTrend:

    @staticmethod
    def seasonal_breakout_returns_trend(prices_array: np.ndarray, LengthMean: int, LengthSnapshot: int, amplitude: int, LenST: int, LenLT: int) -> np.ndarray:

        seasonal_breakout_signal = SeasonalBreakout.seasonal_breakout_returns(prices_array, LengthMean, LengthSnapshot, amplitude)

        trend_signal = Trend.mean_price_ratio(prices_array, LenST, LenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, seasonal_breakout_signal)

class ReturnsDistribution :
    
    @staticmethod
    def skewness(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
        
        return sn.sign_normalization(-skewness_array)

    @staticmethod
    def relative_skewness(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:
        
        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)

        relative_skew = sn.relative_normalization(skewness_array, LenSkew*4)

        return sn.sign_normalization(relative_skew)

    @staticmethod
    def skewness_on_kurtosis_ST(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
        kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
        
        relative_kurt = sn.relative_normalization(kurtosis_array, 2500)

        #TF quand kurt haute, MR quand kurt basse
        skew_on_kurt_signal = np.where(relative_kurt < 0, -skewness_array, skewness_array)

        return sn.sign_normalization(skew_on_kurt_signal)


    @staticmethod
    def skewness_on_kurtosis_LT(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
        kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)

        relative_kurt = sn.relative_normalization(kurtosis_array, 2500)

        #MR quand kurt haute, TF quand kurt basse

        skew_on_kurt_signal = np.where(relative_kurt < 0, skewness_array, -skewness_array)

        return sn.sign_normalization(skew_on_kurt_signal)
    
    @staticmethod
    def relative_skewness_on_kurtosis_ST(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
        kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
        
        relative_skew = sn.relative_normalization(skewness_array, 2500)
        relative_kurt = sn.relative_normalization(kurtosis_array, 2500)

        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, -relative_skew, relative_skew)

        return sn.sign_normalization(relative_skew_on_kurt_signal)

    @staticmethod
    def relative_skewness_on_kurtosis_LT(returns_array: np.ndarray, LenSmooth: int, LenSkew: int) -> np.ndarray:

        skewness_array = RawReturnsDistribution.smoothed_skewness(returns_array, LenSmooth, LenSkew)
        kurtosis_array = RawReturnsDistribution.smoothed_kurtosis(returns_array, LenSmooth, LenSkew)
        
        relative_skew = sn.relative_normalization(skewness_array, 2500)
        relative_kurt = sn.relative_normalization(kurtosis_array, 2500)

        relative_skew_on_kurt_signal = np.where(relative_kurt < 0, relative_skew, -relative_skew)

        return sn.sign_normalization(relative_skew_on_kurt_signal)

class ReturnsDistributionTrend :

    @staticmethod
    def skewness_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        skewness_signal = ReturnsDistribution.skewness(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, skewness_signal)

    @staticmethod
    def relative_skewness_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        relative_skewness_signal = ReturnsDistribution.relative_skewness(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, relative_skewness_signal)

    @staticmethod
    def skewness_on_kurtosis_ST_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        skew_on_kurt_signal = ReturnsDistribution.skewness_on_kurtosis_ST(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)

    @staticmethod
    def skewness_on_kurtosis_LT_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        skew_on_kurt_signal = ReturnsDistribution.skewness_on_kurtosis_LT(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)
    
    @staticmethod
    def relative_skewness_on_kurtosis_ST_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        relative_skew_on_kurt_signal = ReturnsDistribution.relative_skewness_on_kurtosis_ST(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)

    @staticmethod
    def relative_skewness_on_kurtosis_LT_trend(returns_array: np.ndarray, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        relative_skew_on_kurt_signal = ReturnsDistribution.relative_skewness_on_kurtosis_LT(returns_array, LenSmooth, LenSkew)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)
    
class Volatility :

    @staticmethod
    def relative_directional_volatility(returns_array:np.ndarray, LenST:int, LenLT:int, LenVol: int) -> np.ndarray:

        directional_volatility_raw = RawVolatility.smoothed_directional_volatility(returns_array, LenST, LenVol)

        relative_directional_vol_raw = sn.relative_normalization(directional_volatility_raw, LenLT)

        return sn.sign_normalization(relative_directional_vol_raw)

    @staticmethod
    def normalised_directional_volatility(returns_array:np.ndarray, LenST:int, LenLT:int, LenVol: int) -> np.ndarray:

        directional_volatility_raw = RawVolatility.smoothed_directional_volatility(returns_array, LenST, LenVol)

        return sn.rolling_median_normalisation(-directional_volatility_raw, LenLT*8)
    
class VolatilityTrend:

    @staticmethod
    def relative_directional_volatility_trend(returns_array: np.ndarray, LenST:int, LenLT:int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        relative_directional_vol_signal = Volatility.relative_directional_volatility(returns_array, LenST,LenLT, LenVol)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, relative_directional_vol_signal)
    
    @staticmethod
    def normalised_directional_volatility_trend(returns_array: np.ndarray, LenST:int, LenLT:int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> np.ndarray:

        normalised_directional_vol_signal = Volatility.normalised_directional_volatility(returns_array, LenST,LenLT, LenVol)

        trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        return sn.calculate_indicator_on_trend_signal(trend_signal, normalised_directional_vol_signal)


class Seasonality:
    
    def generate_group_mask(seasonal_array: np.ndarray, GroupBy: int, GroupSelected: int):
        # Utiliser les positions des colonnes saisonnières directement
        # Position 0 : 'DayOfWeek', Position 1 : 'WeekOfMonth', Position 2 : 'QuarterOfYear'
        return seasonal_array[:, GroupBy - 1] == GroupSelected

    @staticmethod
    def generate_seasonal_trend_signal(
        returns_array: np.ndarray,
        group_mask_array: np.ndarray, 
        LenST: int, 
        LenLT: int
    ) -> np.ndarray:

        # Extraction des retours sélectionnés en fonction du masque de groupe
        selected_returns_array = returns_array[group_mask_array]
        
        mean_returns = mt.rolling_mean(selected_returns_array, length=LenST, min_length=1)
        mean_roc_raw = mt.rolling_sum(mean_returns, length=LenLT, min_length=4)
        seasonal_trend_signal = sn.sign_normalization(mean_roc_raw)

        return ft.shift_array(seasonal_trend_signal)


    @staticmethod
    def process_trend_signal(
        seasonal_trend_signal: np.ndarray, 
        group_mask_array: np.ndarray,
        shape: tuple
    ) -> np.ndarray:
        
        processed_seasonal_trend_signal = np.zeros(shape, dtype=np.float32)
        processed_seasonal_trend_signal[group_mask_array] = seasonal_trend_signal

        return processed_seasonal_trend_signal
    
    @staticmethod
    def generate_conditioned_seasonal_trend_signal(
        returns_array: np.ndarray,
        group_mask_array: np.ndarray,
        LenST: int, 
        LenLT: int,
        TrendLenST: int, 
        TrendLenLT: int
    ) -> np.ndarray:

        seasonal_trend_signal = Seasonality.generate_seasonal_trend_signal(returns_array, group_mask_array, LenST, LenLT)

        # Calcul de la tendance générale sur l'ensemble des données
        general_trend_signal = Trend.mean_rate_of_change(returns_array, TrendLenST, TrendLenLT)

        # Décalage en arrière de la tendance générale pour éviter le lookahead journalier
        general_trend_signal = ft.shift_array(general_trend_signal)

        return sn.calculate_indicator_on_trend_signal(general_trend_signal[group_mask_array], seasonal_trend_signal)
    
    @staticmethod
    def seasonal_trend( returns_array: np.ndarray,
                        seasonal_array: np.ndarray,
                        GroupBy: int, 
                        GroupSelected: int, 
                        LenST: int, 
                        LenLT: int) -> np.ndarray:

        group_mask_array = Seasonality.generate_group_mask(seasonal_array, GroupBy, GroupSelected)

        seasonal_trend_signal = Seasonality.generate_seasonal_trend_signal(returns_array, group_mask_array, LenST, LenLT)

        processed_seasonal_trend_signal = Seasonality.process_trend_signal(seasonal_trend_signal, 
                                                                           group_mask_array, 
                                                                           returns_array.shape)

        return np.roll(processed_seasonal_trend_signal, -1, axis=0)

class SeasonalityTrend:

    @staticmethod
    def overall_seasonal_trend(returns_array: np.ndarray,
                                seasonal_array: np.ndarray,
                                GroupBy: int, 
                                GroupSelected: int, 
                                LenST: int, 
                                LenLT: int,
                                TrendLenST: int, 
                                TrendLenLT: int        
                            ) -> np.ndarray:

        group_mask_array = Seasonality.generate_group_mask(seasonal_array, GroupBy, GroupSelected)
        
        seasonal_trend_conditioned_signal = Seasonality.generate_conditioned_seasonal_trend_signal(returns_array, 
                                                                                                   group_mask_array, 
                                                                                                   LenST, 
                                                                                                   LenLT, 
                                                                                                   TrendLenST, 
                                                                                                   TrendLenLT)

        processed_seasonal_trend_conditioned_signal = Seasonality.process_trend_signal(seasonal_trend_conditioned_signal, 
                                                                                       group_mask_array, 
                                                                                       returns_array.shape)

        return np.roll(processed_seasonal_trend_conditioned_signal, -1, axis=0)