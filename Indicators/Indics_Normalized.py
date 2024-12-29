import numpy as np
from Indicators.Indics_Raw import *
from Indicators.Indics_Normalization import sign_normalization, calculate_indicator_on_trend_signal, rolling_median_normalisation, relative_normalization
from Utilitary import ArrayFloat, IndicatorFunc, Float32
from collections.abc import Callable
from Metrics import hv_composite, calculate_volatility_adjusted_returns, calculate_equity_curves, log_returns_np, shift_array
from concurrent.futures import ThreadPoolExecutor
from inspect import signature

class IndicatorMetadata:
    def __init__(self, func: IndicatorFunc, params: list[str]) -> None:
        self.func = func
        self.params: list[str] = params

def indic(registry: dict[str, IndicatorMetadata] = {}) -> Callable[[IndicatorFunc], IndicatorFunc]:
    def decorator(func: IndicatorFunc) -> IndicatorFunc:
        params: list[str] = list(signature(func).parameters.keys())[1:]
        registry[func.__name__] = IndicatorMetadata(func, params)
        return func

    return decorator

class IndicatorsMethods:

    _indicators_registry: dict[str, IndicatorMetadata] = {}

    def __init__(self) -> None:
        self.prices_array : ArrayFloat
        self.log_returns_array: ArrayFloat
        self.adjusted_returns_array: ArrayFloat

    def process_param(
        self,  
        func: IndicatorFunc, 
        param: dict[str, int]
        ) -> ArrayFloat:
        return func(self, **param) * self.adjusted_returns_array

    def process_indicator_parallel(
        self,
        func: IndicatorFunc, 
        params: list[dict[str, int]],
        global_executor: ThreadPoolExecutor
        ) -> list[ArrayFloat]:
        def process_single_param(param: dict[str, int]) -> ArrayFloat:
            return self.process_param(func, param)

        results = list(global_executor.map(process_single_param, params))
        return results

    def process_data(self, pct_returns_array: ArrayFloat) -> None:
        self.prices_array = shift_array(returns_array=calculate_equity_curves(returns_array=pct_returns_array))
        self.log_returns_array = shift_array(returns_array=log_returns_np(prices_array=self.prices_array))
        hv_array: ArrayFloat = hv_composite(returns_array=pct_returns_array)
        self.adjusted_returns_array = calculate_volatility_adjusted_returns(
            pct_returns_array, 
            hv_array
        )

    @classmethod
    def get_all_indicators(cls) -> dict[str, IndicatorMetadata]:
        return cls._indicators_registry

    @classmethod
    def determine_params(cls, name: str, params_config: dict[str, dict[str, list[int]]]) -> dict[str, list[int]]:
        metadata = cls._indicators_registry[name]
        params: dict[str, list[int]] = {}
        for param in metadata.params:
            params[param] = params_config.get(name, {}).get(param, [])
        return params

    @indic(_indicators_registry)
    def mean_price_ratio(self, LenST: int, LenLT: int) -> ArrayFloat:
        mean_price_ratio_raw = calculate_mean_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(mean_price_ratio_raw)
    @indic(_indicators_registry)
    def median_price_ratio(self, LenST: int, LenLT: int) -> ArrayFloat:
        median_price_ratio_raw = calculate_median_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(median_price_ratio_raw)
    @indic(_indicators_registry)
    def central_price_ratio(self, LenST: int, LenLT: int) -> ArrayFloat:
        central_price_ratio_raw = calculate_central_price_ratio_raw(self.prices_array, LenST, LenLT)
        return sign_normalization(central_price_ratio_raw)
    @indic(_indicators_registry)
    def mean_rate_of_change(self, LenST: int, LenLT: int) -> ArrayFloat:
        mean_roc_raw = calculate_mean_rate_of_change_raw(self.log_returns_array, LenST, LenLT)
        return sign_normalization(mean_roc_raw)
    @indic(_indicators_registry)
    def median_rate_of_change(self, LenST: int, LenLT: int) -> ArrayFloat:
        median_roc_raw = calculate_median_rate_of_change_raw(self.log_returns_array, LenST, LenLT)
        return sign_normalization(median_roc_raw)
    @indic(_indicators_registry)
    def central_rate_of_change(self, LenST: int, LenLT: int) -> ArrayFloat:
        central_roc_raw = calculate_central_rate_of_change_raw(self.log_returns_array, LenST, LenLT)
        return sign_normalization(central_roc_raw)
    @indic(_indicators_registry)
    def mean_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        mean_price_ratio_macd_raw = calculate_mean_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(mean_price_ratio_macd_raw)
    @indic(_indicators_registry)
    def median_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        median_price_ratio_macd_raw = calculate_median_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(median_price_ratio_macd_raw)
    @indic(_indicators_registry)
    def central_price_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        central_price_ratio_macd_raw = calculate_central_price_macd_raw(self.prices_array, LenST, LenLT, MacdLength)
        return sign_normalization(central_price_ratio_macd_raw)
    @indic(_indicators_registry)
    def mean_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        mean_roc_macd_raw = calculate_mean_rate_of_change_macd_raw(self.log_returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(mean_roc_macd_raw)
    @indic(_indicators_registry)
    def median_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        median_roc_macd_raw = calculate_median_rate_of_change_macd_raw(self.log_returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(median_roc_macd_raw)
    @indic(_indicators_registry)
    def central_rate_of_change_macd(self, LenST: int, LenLT: int, MacdLength: int) -> ArrayFloat:
        central_roc_macd_raw = calculate_central_rate_of_change_macd_raw(self.log_returns_array, LenST, LenLT, MacdLength)
        return sign_normalization(central_roc_macd_raw)
    @indic(_indicators_registry)
    def mean_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        mean_price_ratio_signal = self.mean_price_ratio(TrendLenST, TrendLenLT)
        mean_price_macd_signal = self.mean_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(mean_price_ratio_signal, mean_price_macd_signal)
    @indic(_indicators_registry)
    def median_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        median_price_ratio_signal = self.median_price_ratio(TrendLenST, TrendLenLT)
        median_price_macd_signal = self.median_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(median_price_ratio_signal, median_price_macd_signal)
    @indic(_indicators_registry)
    def central_price_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        central_price_ratio_signal = self.central_price_ratio(TrendLenST, TrendLenLT)
        central_price_macd_signal = self.central_price_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(central_price_ratio_signal, central_price_macd_signal)
    @indic(_indicators_registry)
    def mean_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        mean_roc_trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        mean_roc_macd_signal = self.mean_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(mean_roc_trend_signal, mean_roc_macd_signal)
    @indic(_indicators_registry)
    def median_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        median_roc_trend_signal = self.median_rate_of_change(TrendLenST, TrendLenLT)
        median_roc_macd_signal = self.median_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(median_roc_trend_signal, median_roc_macd_signal)
    @indic(_indicators_registry)
    def central_rate_of_change_macd_trend(self, LenST: int, LenLT: int, MacdLength: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        central_roc_trend_signal = self.central_rate_of_change(TrendLenST, TrendLenLT)
        central_roc_macd_signal = self.central_rate_of_change_macd(LenST, LenLT, MacdLength)
        return calculate_indicator_on_trend_signal(central_roc_trend_signal, central_roc_macd_signal)
    @indic(_indicators_registry)
    def fixed_bias(self, Bias: int) -> ArrayFloat:
        return np.full(self.prices_array.shape, Bias, dtype=Float32)
    @indic(_indicators_registry)
    def mean_price_ratio_normalised(self, SignalLength: int, PLength: int) -> ArrayFloat:
        mean_price_ratio = calculate_mean_price_ratio_raw(self.prices_array, 1, SignalLength)
        return rolling_median_normalisation(-mean_price_ratio, PLength)
    @indic(_indicators_registry)
    def mean_rate_of_change_normalised(self, SignalLength: int, PLength: int) -> ArrayFloat:
        mean_roc = calculate_mean_rate_of_change_raw(self.log_returns_array, 1, SignalLength)
        return rolling_median_normalisation(-mean_roc, PLength)
    @indic(_indicators_registry)
    def mean_price_ratio_normalised_trend(self, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> ArrayFloat:
        mean_reversion_signal = self.mean_price_ratio_normalised(SignalLength, PLength)
        trend_signal = self.mean_price_ratio(LenST, LenLT)
        return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)
    @indic(_indicators_registry)
    def mean_rate_of_change_normalised_trend(self, SignalLength: int, PLength: int, LenST: int, LenLT: int) -> ArrayFloat:
        mean_reversion_signal = self.mean_rate_of_change_normalised(SignalLength, PLength)
        trend_signal = self.mean_rate_of_change(LenST, LenLT)
        return calculate_indicator_on_trend_signal(trend_signal, mean_reversion_signal)
    @indic(_indicators_registry)
    def skewness(self, LenSmooth: int, LenSkew: int) -> ArrayFloat:
        skewness_array = smoothed_skewness(self.log_returns_array, LenSmooth, LenSkew)
        return sign_normalization(-skewness_array)
    @indic(_indicators_registry)
    def relative_skewness(self, LenSmooth: int, LenSkew: int) -> ArrayFloat:
        skewness_array = smoothed_skewness(self.log_returns_array, LenSmooth, LenSkew)
        relative_skew = relative_normalization(skewness_array, LenSkew*4)
        return sign_normalization(relative_skew)
    @indic(_indicators_registry)
    def skewness_on_kurtosis(self, LenSmooth: int, LenSkew: int) -> ArrayFloat:
        skewness_array = smoothed_skewness(self.log_returns_array, LenSmooth, LenSkew)
        kurtosis_array = smoothed_kurtosis(self.log_returns_array, LenSmooth, LenSkew)
        relative_kurt = relative_normalization(kurtosis_array, 2500)
        if LenSkew <= 64:
            skew_on_kurt_signal = np.where(relative_kurt < 0, -skewness_array, skewness_array)
        else:
            skew_on_kurt_signal = np.where(relative_kurt < 0, skewness_array, -skewness_array)
        return sign_normalization(skew_on_kurt_signal)
    @indic(_indicators_registry)
    def relative_skewness_on_kurtosis(self, LenSmooth: int, LenSkew: int) -> ArrayFloat:
        skewness_array = smoothed_skewness(self.log_returns_array, LenSmooth, LenSkew)
        kurtosis_array = smoothed_kurtosis(self.log_returns_array, LenSmooth, LenSkew)
        relative_skew = relative_normalization(skewness_array, 2500)
        relative_kurt = relative_normalization(kurtosis_array, 2500)
        if LenSkew <= 64:
            relative_skew_on_kurt_signal = np.where(relative_kurt < 0, -relative_skew, relative_skew)
        else:
            relative_skew_on_kurt_signal = np.where(relative_kurt < 0, relative_skew, -relative_skew)
        return sign_normalization(relative_skew_on_kurt_signal)
    @indic(_indicators_registry)
    def skewness_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        skewness_signal = self.skewness(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, skewness_signal)
    @indic(_indicators_registry)
    def relative_skewness_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        relative_skewness_signal = self.relative_skewness( LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_skewness_signal)
    @indic(_indicators_registry)
    def skewness_on_kurtosis_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        skew_on_kurt_signal = self.skewness_on_kurtosis(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, skew_on_kurt_signal)
    @indic(_indicators_registry)
    def relative_skewness_on_kurtosis_trend(self, LenSmooth: int, LenSkew: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        relative_skew_on_kurt_signal = self.relative_skewness_on_kurtosis(LenSmooth, LenSkew)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_skew_on_kurt_signal)
    @indic(_indicators_registry)
    def relative_directional_volatility(self, LenSmooth: int, LenRelative: int, LenVol: int) -> ArrayFloat:
        directional_volatility_raw = smoothed_directional_volatility(self.log_returns_array, LenSmooth, LenVol)
        relative_directional_vol_raw = relative_normalization(directional_volatility_raw, LenRelative)
        return sign_normalization(relative_directional_vol_raw)
    @indic(_indicators_registry)
    def normalised_directional_volatility(self, LenSmooth: int, LenNormalization: int, LenVol: int) -> ArrayFloat:
        directional_volatility_raw = smoothed_directional_volatility(self.log_returns_array, LenSmooth, LenVol)
        return rolling_median_normalisation(-directional_volatility_raw, LenNormalization)
    @indic(_indicators_registry)
    def relative_directional_volatility_trend(self, LenSmooth: int, LenRelative: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        relative_directional_vol_signal = self.relative_directional_volatility(LenSmooth, LenRelative, LenVol)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, relative_directional_vol_signal)
    @indic(_indicators_registry)
    def normalised_directional_volatility_trend(self, LenSmooth: int, LenNormalization: int, LenVol: int, TrendLenST: int, TrendLenLT: int) -> ArrayFloat:
        normalised_directional_vol_signal = self.normalised_directional_volatility(LenSmooth, LenNormalization, LenVol)
        trend_signal = self.mean_rate_of_change(TrendLenST, TrendLenLT)
        return calculate_indicator_on_trend_signal(trend_signal, normalised_directional_vol_signal)