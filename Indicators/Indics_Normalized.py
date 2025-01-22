import numpy as np
from Indicators.Indics_Data import ReturnsData
import Indicators.Indics_Raw as raw
import Metrics.Normalization as norm
from TypingConventions import ArrayFloat, Float32
from Indicators.BaseIndicator import BaseIndicator


class IndicatorsNormalized:
    class MeanPriceRatio(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            mean_price_ratio_raw: ArrayFloat = raw.calculate_mean_price_ratio_raw(
                prices_array=returns_data.prices_array, LenST=LenST, LenLT=LenLT
            )
            return norm.sign_normalization(signal_array=mean_price_ratio_raw)

    class MedianPriceRatio(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            median_price_ratio_raw: ArrayFloat = raw.calculate_median_price_ratio_raw(
                prices_array=returns_data.prices_array, LenST=LenST, LenLT=LenLT
            )
            return norm.sign_normalization(signal_array=median_price_ratio_raw)

    class CentralPriceRatio(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            central_price_ratio_raw: ArrayFloat = raw.calculate_central_price_ratio_raw(
                prices_array=returns_data.prices_array, LenST=LenST, LenLT=LenLT
            )
            return norm.sign_normalization(signal_array=central_price_ratio_raw)

    class MeanRateOfChange(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            mean_roc_raw: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
            )
            return norm.sign_normalization(signal_array=mean_roc_raw)

    class MedianRateOfChange(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            median_roc_raw: ArrayFloat = raw.calculate_median_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
            )
            return norm.sign_normalization(signal_array=median_roc_raw)

    class CentralRateOfChange(BaseIndicator):
        def execute(self, returns_data: ReturnsData, LenST: int, LenLT: int) -> ArrayFloat:
            central_roc_raw: ArrayFloat = raw.calculate_central_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
            )
            return norm.sign_normalization(signal_array=central_roc_raw)

    class MeanPriceMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            mean_price_ratio_macd_raw: ArrayFloat = raw.calculate_mean_price_macd_raw(
                prices_array=returns_data.prices_array,
                LenST=LenST,
                LenLT=LenLT,
                MacdLength=MacdLength,
            )
            return norm.sign_normalization(signal_array=mean_price_ratio_macd_raw)

    class MedianPriceMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            median_price_ratio_macd_raw: ArrayFloat = (
                raw.calculate_median_price_macd_raw(
                    prices_array=returns_data.prices_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.sign_normalization(signal_array=median_price_ratio_macd_raw)

    class CentralPriceMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            central_price_ratio_macd_raw: ArrayFloat = (
                raw.calculate_central_price_macd_raw(
                    prices_array=returns_data.prices_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.sign_normalization(signal_array=central_price_ratio_macd_raw)

    class MeanRateOfChangeMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            mean_roc_macd_raw: ArrayFloat = raw.calculate_mean_rate_of_change_macd_raw(
                returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
                MacdLength=MacdLength,
            )
            return norm.sign_normalization(signal_array=mean_roc_macd_raw)

    class MedianRateOfChangeMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            median_roc_macd_raw: ArrayFloat = (
                raw.calculate_median_rate_of_change_macd_raw(
                    returns_array=returns_data.log_returns_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.sign_normalization(signal_array=median_roc_macd_raw)

    class CentralRateOfChangeMACD(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenST: int, LenLT: int, MacdLength: int
        ) -> ArrayFloat:
            central_roc_macd_raw: ArrayFloat = (
                raw.calculate_central_rate_of_change_macd_raw(
                    returns_array=returns_data.log_returns_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.sign_normalization(signal_array=central_roc_macd_raw)

    class MeanPriceMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            mean_price_ratio_signal: ArrayFloat = raw.calculate_mean_price_ratio_raw(
                prices_array=returns_data.prices_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            mean_price_macd_signal: ArrayFloat = raw.calculate_mean_price_macd_raw(
                prices_array=returns_data.prices_array,
                LenST=LenST,
                LenLT=LenLT,
                MacdLength=MacdLength,
            )

            return norm.calculate_indicator_on_trend_signal(
                trend_signal=mean_price_ratio_signal,
                indicator_signal=mean_price_macd_signal,
            )

    class MedianPriceMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            median_price_ratio_signal: ArrayFloat = (
                raw.calculate_median_price_ratio_raw(
                    prices_array=returns_data.prices_array,
                    LenST=TrendLenST,
                    LenLT=TrendLenLT,
                )
            )
            median_price_macd_signal: ArrayFloat = raw.calculate_median_price_macd_raw(
                prices_array=returns_data.prices_array,
                LenST=LenST,
                LenLT=LenLT,
                MacdLength=MacdLength,
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=median_price_ratio_signal,
                indicator_signal=median_price_macd_signal,
            )

    class CentralPriceMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            central_price_ratio_signal: ArrayFloat = (
                raw.calculate_central_price_ratio_raw(
                    prices_array=returns_data.prices_array,
                    LenST=TrendLenST,
                    LenLT=TrendLenLT,
                )
            )
            central_price_macd_signal: ArrayFloat = (
                raw.calculate_central_price_macd_raw(
                    prices_array=returns_data.prices_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=central_price_ratio_signal,
                indicator_signal=central_price_macd_signal,
            )

    class MeanRateOfChangeMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            mean_roc_trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            mean_roc_macd_signal: ArrayFloat = (
                raw.calculate_mean_rate_of_change_macd_raw(
                    returns_array=returns_data.log_returns_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=mean_roc_trend_signal,
                indicator_signal=mean_roc_macd_signal,
            )

    class MedianRateOfChangeMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            median_roc_trend_signal: ArrayFloat = (
                raw.calculate_median_rate_of_change_raw(
                    log_returns_array=returns_data.log_returns_array,
                    LenST=TrendLenST,
                    LenLT=TrendLenLT,
                )
            )
            median_roc_macd_signal: ArrayFloat = (
                raw.calculate_median_rate_of_change_macd_raw(
                    returns_array=returns_data.log_returns_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=median_roc_trend_signal,
                indicator_signal=median_roc_macd_signal,
            )

    class CentralRateOfChangeMACDTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenST: int,
            LenLT: int,
            MacdLength: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            central_roc_trend_signal: ArrayFloat = (
                raw.calculate_central_rate_of_change_raw(
                    log_returns_array=returns_data.log_returns_array,
                    LenST=TrendLenST,
                    LenLT=TrendLenLT,
                )
            )
            central_roc_macd_signal: ArrayFloat = (
                raw.calculate_central_rate_of_change_macd_raw(
                    returns_array=returns_data.log_returns_array,
                    LenST=LenST,
                    LenLT=LenLT,
                    MacdLength=MacdLength,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=central_roc_trend_signal,
                indicator_signal=central_roc_macd_signal,
            )

    class FixedBias(BaseIndicator):
        def execute(self, returns_data: ReturnsData, Bias: int) -> ArrayFloat:
            return np.full(returns_data.prices_array.shape, Bias, dtype=Float32)

    class MeanPriceRatioNormalised(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, SignalLength: int, PLength: int
        ) -> ArrayFloat:
            normalised_price_ratio: ArrayFloat = (
                raw.calculate_normalised_mean_price_ratio_raw(
                    prices_array=returns_data.prices_array,
                    SignalLength=SignalLength,
                    PLength=PLength,
                )
            )
            return norm.limit_normalization(signal_array=normalised_price_ratio)

    class MeanRateOfChangeNormalised(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, SignalLength: int, PLength: int
        ) -> ArrayFloat:
            normalised_roc: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=returns_data.log_returns_array,
                    SignalLength=SignalLength,
                    PLength=PLength,
                )
            )

            return norm.limit_normalization(signal_array=normalised_roc)

    class MeanRateOfChangeNormalisedTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            SignalLength: int,
            PLength: int,
            LenST: int,
            LenLT: int,
        ) -> ArrayFloat:
            normalised_roc: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=returns_data.log_returns_array,
                    SignalLength=SignalLength,
                    PLength=PLength,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
            )
            normalised_on_trend_signal: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=normalised_roc
                )
            )
            return norm.limit_normalization(signal_array=normalised_on_trend_signal)

    class MeanPriceRatioNormalisedTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            SignalLength: int,
            PLength: int,
            LenST: int,
            LenLT: int,
        ) -> ArrayFloat:
            normalised_ratio: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=returns_data.log_returns_array,
                    SignalLength=SignalLength,
                    PLength=PLength,
                )
            )
            trend_signal = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=LenST,
                LenLT=LenLT,
            )
            normalised_on_trend_signal: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=normalised_ratio
                )
            )
            return norm.limit_normalization(signal_array=normalised_on_trend_signal)

    class Skewness(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenSkew: int
        ) -> ArrayFloat:
            skewness_array: ArrayFloat = raw.smoothed_skewness(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            return norm.sign_normalization(signal_array=-skewness_array)

    class RelativeSkewness(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenSkew: int
        ) -> ArrayFloat:
            relative_skew: ArrayFloat = raw.calculate_relative_skewness(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            return norm.sign_normalization(signal_array=relative_skew)

    class SkewnessOnKurtosis(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenSkew: int
        ) -> ArrayFloat:
            skew_on_kurt_signal: ArrayFloat = raw.calculate_skew_on_kurtosis(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            return norm.sign_normalization(signal_array=skew_on_kurt_signal)

    class RelativeSkewnessOnKurtosis(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenSkew: int
        ) -> ArrayFloat:
            relative_skew_on_kurt_signal: ArrayFloat = (
                raw.calculate_relative_skew_on_kurtosis(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenSkew=LenSkew,
                )
            )
            return norm.sign_normalization(signal_array=relative_skew_on_kurt_signal)

    class SkewnessTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenSkew: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            skewness_signal: ArrayFloat = raw.smoothed_skewness(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            skew_on_trend_signal: ArrayFloat = norm.calculate_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=skewness_signal
            )
            return norm.sign_normalization(signal_array=skew_on_trend_signal)

    class RelativeSkewnessTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenSkew: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            relative_skewness_signal: ArrayFloat = raw.calculate_relative_skewness(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            relative_skew_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=relative_skewness_signal
                )
            )

            return norm.sign_normalization(signal_array=relative_skew_on_trend)

    class SkewnessOnKurtosisTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenSkew: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            skew_on_kurt_signal: ArrayFloat = raw.calculate_skew_on_kurtosis(
                log_returns_array=returns_data.log_returns_array,
                LenSmooth=LenSmooth,
                LenSkew=LenSkew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=skew_on_kurt_signal
            )

    class RelativeSkewnessOnKurtosisTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenSkew: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            relative_skew_on_kurt_signal: ArrayFloat = (
                raw.calculate_relative_skew_on_kurtosis(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenSkew=LenSkew,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            relative_skew_on_kurt_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal,
                    indicator_signal=relative_skew_on_kurt_signal,
                )
            )

            return norm.limit_normalization(signal_array=relative_skew_on_kurt_on_trend)

    class RelativeDirectionalVolatility(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenRelative: int, LenVol: int
        ) -> ArrayFloat:
            relative_directional_vol_signal: ArrayFloat = (
                raw.relative_directional_volatility(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenVol=LenVol,
                    LenRelative=LenRelative,
                )
            )
            return norm.sign_normalization(signal_array=relative_directional_vol_signal)

    class NormalisedDirectionalVolatility(BaseIndicator):
        def execute(
            self, returns_data: ReturnsData, LenSmooth: int, LenNormalization: int, LenVol: int
        ) -> ArrayFloat:
            normalised_directional_vol: ArrayFloat = (
                raw.normalised_directional_volatility(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenVol=LenVol,
                    LenNormalization=LenNormalization,
                )
            )

            return norm.limit_normalization(signal_array=normalised_directional_vol)

    class RelativeDirectionalVolatilityTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenRelative: int,
            LenVol: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            relative_directional_vol_signal: ArrayFloat = (
                raw.relative_directional_volatility(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenVol=LenVol,
                    LenRelative=LenRelative,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )

            relative_directional_vol_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal,
                    indicator_signal=relative_directional_vol_signal,
                )
            )
            return norm.limit_normalization(
                signal_array=relative_directional_vol_on_trend
            )

    class NormalisedDirectionalVolatilityTrend(BaseIndicator):
        def execute(
            self,
            returns_data: ReturnsData,
            LenSmooth: int,
            LenNormalization: int,
            LenVol: int,
            TrendLenST: int,
            TrendLenLT: int,
        ) -> ArrayFloat:
            normalised_directional_vol: ArrayFloat = (
                raw.normalised_directional_volatility(
                    log_returns_array=returns_data.log_returns_array,
                    LenSmooth=LenSmooth,
                    LenVol=LenVol,
                    LenNormalization=LenNormalization,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=returns_data.log_returns_array,
                LenST=TrendLenST,
                LenLT=TrendLenLT,
            )
            normalised_directional_vol_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal,
                    indicator_signal=normalised_directional_vol,
                )
            )
            return norm.limit_normalization(
                signal_array=normalised_directional_vol_on_trend
            )
