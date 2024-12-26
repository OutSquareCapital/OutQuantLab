import numpy as np
from .Indics_Raw import *
from .Indics_Normalization import sign_normalization, calculate_indicator_on_trend_signal, rolling_median_normalisation, relative_normalization
from Files import NDArrayFloat, IndicatorFunc
from inspect import signature

class IndicatorsMethods:
    def __init__(self) -> None:
        self.prices_array : NDArrayFloat
        self.returns_array: NDArrayFloat

    @classmethod
    def get_all_signals(cls) -> dict[str, IndicatorFunc]:
        signals: dict[str, IndicatorFunc] = {}
        for name, func in vars(cls).items():
            if callable(func) and not name.startswith('_') and name not in ['get_all_signals', 'determine_params']:
                signals[name] = func # type: ignore
        return signals

    @classmethod
    def determine_params(cls, name: str, params_config: dict[str, dict[str, list[int]]]) -> dict[str, list[int]]:
        method = getattr(cls, name)
        func_signature = signature(method).parameters
        param_values = params_config.get(name, {})
        return {
            param_name: param_values.get(param_name, [])
            for param_name in func_signature.keys()
            if param_name != 'self'
        }

    def mean_price_ratio(self, LenST: int, LenLT: int) -> NDArrayFloat:
        mean_price_ratio_raw = calculate_mean_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(mean_price_ratio_raw)

    def median_price_ratio(self, LenST: int, LenLT: int) -> NDArrayFloat:
        median_price_ratio_raw = calculate_median_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(median_price_ratio_raw)

    def central_price_ratio(self, LenST: int, LenLT: int) -> NDArrayFloat:
        central_price_ratio_raw = calculate_central_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(central_price_ratio_raw)

    def mean_rate_of_change(self, LenST: int, LenLT: int) -> NDArrayFloat:
        mean_roc_raw = calculate_mean_rate_of_change_raw(self.returns_array, LenST, LenLT)
        return sign_normalization(mean_roc_raw)

    def median_rate_of_change(self, LenST: int, LenLT: int) -> NDArrayFloat:
        median_roc_raw = calculate_median_rate_of_change_raw(self.returns_array, LenST, LenLT)
        return sign_normalization(median_roc_raw)

    def central_rate_of_change(self, LenST: int, LenLT: int) -> NDArrayFloat:
        central_roc_raw = calculate_central_rate_of_change_raw(self.returns_array, LenST, LenLT)
        return sign_normalization(central_roc_raw)

    def mean_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        mean_price_ratio_macd_raw = calculate_mean_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(mean_price_ratio_macd_raw)

    def median_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        median_price_ratio_macd_raw = calculate_median_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(median_price_ratio_macd_raw)

    def central_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        central_price_ratio_macd_raw = calculate_central_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(central_price_ratio_macd_raw)

    def mean_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        mean_roc_macd_raw = calculate_mean_rate_of_change_macd_raw(self.returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(mean_roc_macd_raw)

    def median_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        median_roc_macd_raw = calculate_median_rate_of_change_macd_raw(self.returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(median_roc_macd_raw)

    def central_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> NDArrayFloat:
        central_roc_macd_raw = calculate_central_rate_of_change_macd_raw(self.returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(central_roc_macd_raw)

    def mean_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        mean_price_ratio_signal = self.mean_price_ratio(TrendLenST, TrendLenLT)
        mean_price_macd_signal = self.mean_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(mean_price_ratio_signal, mean_price_macd_signal)

    def median_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        median_price_ratio_signal = self.median_price_ratio(TrendLenST, TrendLenLT)
        median_price_macd_signal = self.median_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(median_price_ratio_signal, median_price_macd_signal)

    def central_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        central_price_ratio_signal = self.central_price_ratio(TrendLenST, TrendLenLT)
        central_price_macd_signal = self.central_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(central_price_ratio_signal, central_price_macd_signal)

    def mean_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        mean_roc_trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        mean_roc_macd_signal = self.mean_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(mean_roc_trend_signal, mean_roc_macd_signal)

    def median_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        median_roc_trend_signal = self.median_rate_of_change(TrendLenST, TrendLenLT)
        median_roc_macd_signal = self.median_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(median_roc_trend_signal, median_roc_macd_signal)

    def central_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        central_roc_trend_signal = self.central_rate_of_change(TrendLenST, TrendLenLT)
        central_roc_macd_signal = self.central_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(central_roc_trend_signal, central_roc_macd_signal)

    def fixed_bias(self, Bias: int) -> NDArrayFloat:
        return np.full_like(self, Bias, dtype=np.float32)

    def mean_price_ratio_normalised(self, SignalLength: int, PLength: int) -> NDArrayFloat:
        mean_price_ratio = calculate_mean_price_ratio_raw(self.prices_array, 1, SignalLength)
        return rolling_median_normalisation(-mean_price_ratio, PLength)

    def mean_rate_of_change_normalised(self, SignalLength: int, PLength: int) -> NDArrayFloat:
        mean_roc = calculate_mean_rate_of_change_raw(self.returns_array, 1, SignalLength)
        return rolling_median_normalisation(-mean_roc, PLength)

    def mean_price_ratio_normalised_trend(self, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> NDArrayFloat:
        mean_reversion_signal = self.mean_price_ratio_normalised(SignalLength, PLength)
        trend_signal = self.mean_price_ratio(LenST, LenLT)
        return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)

    def mean_rate_of_change_normalised_trend(self, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> NDArrayFloat:
        mean_reversion_signal = self.mean_rate_of_change_normalised(SignalLength, PLength)
        trend_signal = self.mean_rate_of_change(LenST, LenLT)
        return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)

    def skewness(self, LenSmooth: int, LenSkew: int) -> NDArrayFloat:
        skewness_array = smoothed_skewness(self.returns_array, LenSmooth, LenSkew)
        return sign_normalization(-skewness_array)

    def relative_skewness(self, LenSmooth: int, LenSkew: int) -> NDArrayFloat:
        skewness_array = smoothed_skewness(self.returns_array, LenSmooth, LenSkew)
        relative_skew = relative_normalization(skewness_array, LenSkew*4)
        return sign_normalization(relative_skew)

    def skewness_on_kurtosis(self, LenSmooth: int, LenSkew: int) -> NDArrayFloat:
        skewness_array = smoothed_skewness(self.returns_array, LenSmooth, LenSkew)
        kurtosis_array = smoothed_kurtosis(self.returns_array, LenSmooth, LenSkew)
        relative_kurt = relative_normalization(kurtosis_array, 2500)
        if LenSkew <= 64:
            skew_on_kurt_signal = np.where(relative_kurt < 0, -skewness_array, skewness_array)
        else:
            skew_on_kurt_signal = np.where(relative_kurt < 0, skewness_array, -skewness_array)
        return sign_normalization(skew_on_kurt_signal)

    def relative_skewness_on_kurtosis(self, LenSmooth: int, LenSkew: int) -> NDArrayFloat:
        skewness_array = smoothed_skewness(self.returns_array, LenSmooth, LenSkew)
        kurtosis_array = smoothed_kurtosis(self.returns_array, LenSmooth, LenSkew)
        relative_skew = relative_normalization(skewness_array, 2500)
        relative_kurt = relative_normalization(kurtosis_array, 2500)
        if LenSkew <= 64:
            relative_skew_on_kurt_signal = np.where(relative_kurt < 0, -relative_skew, relative_skew)
        else:
            relative_skew_on_kurt_signal = np.where(relative_kurt < 0, relative_skew, -relative_skew)
        return sign_normalization(relative_skew_on_kurt_signal)

    def skewness_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        skewness_signal = self.skewness(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, skewness_signal)

    def relative_skewness_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        relative_skewness_signal = self.relative_skewness( LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_skewness_signal)

    def skewness_on_kurtosis_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        skew_on_kurt_signal = self.skewness_on_kurtosis(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)

    def relative_skewness_on_kurtosis_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        relative_skew_on_kurt_signal = self.relative_skewness_on_kurtosis(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)

    def relative_directional_volatility(self, LenSmooth: int, LenRelative: int, LenVol: int) -> NDArrayFloat:
        directional_volatility_raw = smoothed_directional_volatility(self.returns_array, LenSmooth, LenVol)
        relative_directional_vol_raw = relative_normalization(directional_volatility_raw, LenRelative)
        return sign_normalization(relative_directional_vol_raw)

    def normalised_directional_volatility(self, LenSmooth: int, LenNormalization: int, LenVol: int) -> NDArrayFloat:
        directional_volatility_raw = smoothed_directional_volatility(self.returns_array, LenSmooth, LenVol)
        return rolling_median_normalisation(-directional_volatility_raw, LenNormalization)

    def relative_directional_volatility_trend(self, LenSmooth: int, LenRelative: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        relative_directional_vol_signal = self.relative_directional_volatility(LenSmooth, LenRelative, LenVol)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_directional_vol_signal)

    def normalised_directional_volatility_trend(self, LenSmooth: int, LenNormalization: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> NDArrayFloat:
        normalised_directional_vol_signal = self.normalised_directional_volatility(LenSmooth, LenNormalization, LenVol)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, normalised_directional_vol_signal)