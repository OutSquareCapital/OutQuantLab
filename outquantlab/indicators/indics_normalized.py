import numpy as np

import outquantlab.indicators.indics_raw as raw
import outquantlab.metrics.normalization as norm
from outquantlab.indicators.base_indicator import BaseIndic
from outquantlab.typing_conventions import ArrayFloat, Float32


class IndicatorsNormalized:
    class MeanPriceRatio(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            mean_price_ratio_raw: ArrayFloat = raw.calculate_mean_price_ratio_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=mean_price_ratio_raw)

    class MedianPriceRatio(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            median_price_ratio_raw: ArrayFloat = raw.calculate_median_price_ratio_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=median_price_ratio_raw)

    class CentralPriceRatio(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            central_price_ratio_raw: ArrayFloat = raw.calculate_central_price_ratio_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=central_price_ratio_raw)

    class MeanRateOfChange(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            mean_roc_raw: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=mean_roc_raw)

    class MedianRateOfChange(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            median_roc_raw: ArrayFloat = raw.calculate_median_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=median_roc_raw)

    class CentralRateOfChange(BaseIndic):
        def execute(self, len_st: int, len_lt: int) -> ArrayFloat:
            central_roc_raw: ArrayFloat = raw.calculate_central_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            return norm.sign_normalization(signal_array=central_roc_raw)

    class MeanPriceMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            mean_price_ratio_macd_raw: ArrayFloat = raw.calculate_mean_price_macd_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
            return norm.sign_normalization(signal_array=mean_price_ratio_macd_raw)

    class MedianPriceMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            median_price_ratio_macd_raw: ArrayFloat = (
                raw.calculate_median_price_macd_raw(
                    prices_array=self.returns_data.prices_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.sign_normalization(signal_array=median_price_ratio_macd_raw)

    class CentralPriceMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            central_price_ratio_macd_raw: ArrayFloat = (
                raw.calculate_central_price_macd_raw(
                    prices_array=self.returns_data.prices_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.sign_normalization(signal_array=central_price_ratio_macd_raw)

    class MeanRateOfChangeMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            mean_roc_macd_raw: ArrayFloat = raw.calculate_mean_rate_of_change_macd_raw(
                returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
            return norm.sign_normalization(signal_array=mean_roc_macd_raw)

    class MedianRateOfChangeMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            median_roc_macd_raw: ArrayFloat = (
                raw.calculate_median_rate_of_change_macd_raw(
                    returns_array=self.returns_data.log_returns_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.sign_normalization(signal_array=median_roc_macd_raw)

    class CentralRateOfChangeMacd(BaseIndic):
        def execute(self, len_st: int, len_lt: int, len_macd: int) -> ArrayFloat:
            central_roc_macd_raw: ArrayFloat = (
                raw.calculate_central_rate_of_change_macd_raw(
                    returns_array=self.returns_data.log_returns_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.sign_normalization(signal_array=central_roc_macd_raw)

    class MeanPriceMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            mean_price_ratio_signal: ArrayFloat = raw.calculate_mean_price_ratio_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            mean_price_macd_signal: ArrayFloat = raw.calculate_mean_price_macd_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )

            return norm.calculate_indicator_on_trend_signal(
                trend_signal=mean_price_ratio_signal,
                indicator_signal=mean_price_macd_signal,
            )

    class MedianPriceMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            median_price_ratio_signal: ArrayFloat = (
                raw.calculate_median_price_ratio_raw(
                    prices_array=self.returns_data.prices_array,
                    len_st=len_trend_st,
                    len_lt=len_trend_lt,
                )
            )
            median_price_macd_signal: ArrayFloat = raw.calculate_median_price_macd_raw(
                prices_array=self.returns_data.prices_array,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=median_price_ratio_signal,
                indicator_signal=median_price_macd_signal,
            )

    class CentralPriceMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            central_price_ratio_signal: ArrayFloat = (
                raw.calculate_central_price_ratio_raw(
                    prices_array=self.returns_data.prices_array,
                    len_st=len_trend_st,
                    len_lt=len_trend_lt,
                )
            )
            central_price_macd_signal: ArrayFloat = (
                raw.calculate_central_price_macd_raw(
                    prices_array=self.returns_data.prices_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=central_price_ratio_signal,
                indicator_signal=central_price_macd_signal,
            )

    class MeanRateOfChangeMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            mean_roc_trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            mean_roc_macd_signal: ArrayFloat = (
                raw.calculate_mean_rate_of_change_macd_raw(
                    returns_array=self.returns_data.log_returns_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=mean_roc_trend_signal,
                indicator_signal=mean_roc_macd_signal,
            )

    class MedianRateOfChangeMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            median_roc_trend_signal: ArrayFloat = (
                raw.calculate_median_rate_of_change_raw(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_st=len_trend_st,
                    len_lt=len_trend_lt,
                )
            )
            median_roc_macd_signal: ArrayFloat = (
                raw.calculate_median_rate_of_change_macd_raw(
                    returns_array=self.returns_data.log_returns_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=median_roc_trend_signal,
                indicator_signal=median_roc_macd_signal,
            )

    class CentralRateOfChangeMacdTrend(BaseIndic):
        def execute(
            self,
            len_st: int,
            len_lt: int,
            len_macd: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            central_roc_trend_signal: ArrayFloat = (
                raw.calculate_central_rate_of_change_raw(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_st=len_trend_st,
                    len_lt=len_trend_lt,
                )
            )
            central_roc_macd_signal: ArrayFloat = (
                raw.calculate_central_rate_of_change_macd_raw(
                    returns_array=self.returns_data.log_returns_array,
                    len_st=len_st,
                    len_lt=len_lt,
                    len_macd=len_macd,
                )
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=central_roc_trend_signal,
                indicator_signal=central_roc_macd_signal,
            )

    class FixedBias(BaseIndic):
        def execute(self, Bias: int) -> ArrayFloat:
            return np.full(self.returns_data.prices_array.shape, Bias, dtype=Float32)

    class MeanPriceRatioNormalised(BaseIndic):
        def execute(self, len_signal: int, len_norm: int) -> ArrayFloat:
            normalised_price_ratio: ArrayFloat = (
                raw.calculate_normalised_mean_price_ratio_raw(
                    prices_array=self.returns_data.prices_array,
                    len_signal=len_signal,
                    len_norm=len_norm,
                )
            )
            return norm.limit_normalization(signal_array=normalised_price_ratio)

    class MeanRateOfChangeNormalised(BaseIndic):
        def execute(self, len_signal: int, len_norm: int) -> ArrayFloat:
            normalised_roc: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_signal=len_signal,
                    len_norm=len_norm,
                )
            )

            return norm.limit_normalization(signal_array=normalised_roc)

    class MeanRateOfChangeNormalisedTrend(BaseIndic):
        def execute(
            self,
            len_signal: int,
            len_norm: int,
            len_st: int,
            len_lt: int,
        ) -> ArrayFloat:
            normalised_roc: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_signal=len_signal,
                    len_norm=len_norm,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            normalised_on_trend_signal: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=normalised_roc
                )
            )
            return norm.limit_normalization(signal_array=normalised_on_trend_signal)

    class MeanPriceRatioNormalisedTrend(BaseIndic):
        def execute(
            self,
            len_signal: int,
            len_norm: int,
            len_st: int,
            len_lt: int,
        ) -> ArrayFloat:
            normalised_ratio: ArrayFloat = (
                raw.calculate_normalised_mean_rate_of_change_raw(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_signal=len_signal,
                    len_norm=len_norm,
                )
            )
            trend_signal = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_st,
                len_lt=len_lt,
            )
            normalised_on_trend_signal: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=normalised_ratio
                )
            )
            return norm.limit_normalization(signal_array=normalised_on_trend_signal)

    class Skewness(BaseIndic):
        def execute(self, len_smooth: int, len_skew: int) -> ArrayFloat:
            skewness_array: ArrayFloat = raw.smoothed_skewness(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            return norm.sign_normalization(signal_array=-skewness_array)

    class RelativeSkewness(BaseIndic):
        def execute(self, len_smooth: int, len_skew: int) -> ArrayFloat:
            relative_skew: ArrayFloat = raw.calculate_relative_skewness(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            return norm.sign_normalization(signal_array=relative_skew)

    class SkewnessOnKurtosis(BaseIndic):
        def execute(self, len_smooth: int, len_skew: int) -> ArrayFloat:
            skew_on_kurt_signal: ArrayFloat = raw.calculate_skew_on_kurtosis(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            return norm.sign_normalization(signal_array=skew_on_kurt_signal)

    class RelativeSkewnessOnKurtosis(BaseIndic):
        def execute(self, len_smooth: int, len_skew: int) -> ArrayFloat:
            relative_skew_on_kurt_signal: ArrayFloat = (
                raw.calculate_relative_skew_on_kurtosis(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_skew=len_skew,
                )
            )
            return norm.sign_normalization(signal_array=relative_skew_on_kurt_signal)

    class SkewnessTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_skew: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            skewness_signal: ArrayFloat = raw.smoothed_skewness(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            skew_on_trend_signal: ArrayFloat = norm.calculate_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=skewness_signal
            )
            return norm.sign_normalization(signal_array=skew_on_trend_signal)

    class RelativeSkewnessTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_skew: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            relative_skewness_signal: ArrayFloat = raw.calculate_relative_skewness(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            relative_skew_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal, indicator_signal=relative_skewness_signal
                )
            )

            return norm.sign_normalization(signal_array=relative_skew_on_trend)

    class SkewnessOnKurtosisTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_skew: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            skew_on_kurt_signal: ArrayFloat = raw.calculate_skew_on_kurtosis(
                log_returns_array=self.returns_data.log_returns_array,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            return norm.calculate_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=skew_on_kurt_signal
            )

    class RelativeSkewnessOnKurtosisTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_skew: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            relative_skew_on_kurt_signal: ArrayFloat = (
                raw.calculate_relative_skew_on_kurtosis(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_skew=len_skew,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
            relative_skew_on_kurt_on_trend: ArrayFloat = (
                norm.calculate_indicator_on_trend_signal(
                    trend_signal=trend_signal,
                    indicator_signal=relative_skew_on_kurt_signal,
                )
            )

            return norm.limit_normalization(signal_array=relative_skew_on_kurt_on_trend)

    class RelativeDirectionalVolatility(BaseIndic):
        def execute(
            self, len_smooth: int, len_relative: int, len_vol: int
        ) -> ArrayFloat:
            relative_directional_vol_signal: ArrayFloat = (
                raw.relative_directional_volatility(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_vol=len_vol,
                    len_relative=len_relative,
                )
            )
            return norm.sign_normalization(signal_array=relative_directional_vol_signal)

    class NormalisedDirectionalVolatility(BaseIndic):
        def execute(self, len_smooth: int, len_norm: int, len_vol: int) -> ArrayFloat:
            normalised_directional_vol: ArrayFloat = (
                raw.normalised_directional_volatility(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_vol=len_vol,
                    len_norm=len_norm,
                )
            )

            return norm.limit_normalization(signal_array=normalised_directional_vol)

    class RelativeDirectionalVolatilityTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_relative: int,
            len_vol: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            relative_directional_vol_signal: ArrayFloat = (
                raw.relative_directional_volatility(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_vol=len_vol,
                    len_relative=len_relative,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
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

    class NormalisedDirectionalVolatilityTrend(BaseIndic):
        def execute(
            self,
            len_smooth: int,
            len_norm: int,
            len_vol: int,
            len_trend_st: int,
            len_trend_lt: int,
        ) -> ArrayFloat:
            normalised_directional_vol: ArrayFloat = (
                raw.normalised_directional_volatility(
                    log_returns_array=self.returns_data.log_returns_array,
                    len_smooth=len_smooth,
                    len_vol=len_vol,
                    len_norm=len_norm,
                )
            )
            trend_signal: ArrayFloat = raw.calculate_mean_rate_of_change_raw(
                log_returns_array=self.returns_data.log_returns_array,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
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
