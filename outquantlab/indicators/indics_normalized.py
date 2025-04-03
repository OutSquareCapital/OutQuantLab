from typing import Protocol

import outquantlab.indicators.indics_raw as raw
import outquantlab.metrics as mt
from outquantlab.indicators.indics_config import BaseIndic
from outquantlab.structures import arrays


class AssetsData(Protocol):
    prices: arrays.ArrayFloat
    log_returns: arrays.ArrayFloat


INDICATOR_REGISTRY: dict[str, type[BaseIndic]] = {}


def _register_indicator(cls: type[BaseIndic]) -> type[BaseIndic]:
    INDICATOR_REGISTRY[cls.__name__] = cls
    return cls


@_register_indicator
class MeanPriceRatio(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        mean_price_ratio_raw: arrays.ArrayFloat = raw.get_mean_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=mean_price_ratio_raw)


@_register_indicator
class MedianPriceRatio(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        median_price_ratio_raw: arrays.ArrayFloat = raw.get_median_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=median_price_ratio_raw)


@_register_indicator
class CentralPriceRatio(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        central_price_ratio_raw: arrays.ArrayFloat = raw.get_central_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=central_price_ratio_raw)


@_register_indicator
class MeanRateOfChange(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        mean_roc_raw: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=mean_roc_raw)


@_register_indicator
class MedianRateOfChange(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        median_roc_raw: arrays.ArrayFloat = raw.get_median_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=median_roc_raw)


@_register_indicator
class CentralRateOfChange(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int
    ) -> arrays.ArrayFloat:
        central_roc_raw: arrays.ArrayFloat = raw.get_central_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
        )
        return mt.sign_normalization(signal_array=central_roc_raw)


@_register_indicator
class MeanPriceMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        mean_price_ratio_macd_raw: arrays.ArrayFloat = raw.get_mean_price_macd_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.sign_normalization(signal_array=mean_price_ratio_macd_raw)


@_register_indicator
class MedianPriceMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        median_price_ratio_macd_raw: arrays.ArrayFloat = raw.get_median_price_macd_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.sign_normalization(signal_array=median_price_ratio_macd_raw)


@_register_indicator
class CentralPriceMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        central_price_ratio_macd_raw: arrays.ArrayFloat = (
            raw.get_central_price_macd_raw(
                prices_array=data_arrays.prices,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
        )
        return mt.sign_normalization(signal_array=central_price_ratio_macd_raw)


@_register_indicator
class MeanRateOfChangeMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        mean_roc_macd_raw: arrays.ArrayFloat = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.sign_normalization(signal_array=mean_roc_macd_raw)


@_register_indicator
class MedianRateOfChangeMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        median_roc_macd_raw: arrays.ArrayFloat = raw.get_median_rate_of_change_macd_raw(
            returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.sign_normalization(signal_array=median_roc_macd_raw)


@_register_indicator
class CentralRateOfChangeMacd(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_st: int, len_lt: int, len_macd: int
    ) -> arrays.ArrayFloat:
        central_roc_macd_raw: arrays.ArrayFloat = (
            raw.get_central_rate_of_change_macd_raw(
                returns_array=data_arrays.log_returns,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
        )
        return mt.sign_normalization(signal_array=central_roc_macd_raw)


@_register_indicator
class MeanPriceMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        mean_price_ratio_signal: arrays.ArrayFloat = raw.get_mean_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        mean_price_macd_signal: arrays.ArrayFloat = raw.get_mean_price_macd_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )

        return mt.get_indicator_on_trend_signal(
            trend_signal=mean_price_ratio_signal,
            indicator_signal=mean_price_macd_signal,
        )


@_register_indicator
class MedianPriceMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        median_price_ratio_signal: arrays.ArrayFloat = raw.get_median_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        median_price_macd_signal: arrays.ArrayFloat = raw.get_median_price_macd_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=median_price_ratio_signal,
            indicator_signal=median_price_macd_signal,
        )


@_register_indicator
class CentralPriceMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        central_price_ratio_signal: arrays.ArrayFloat = raw.get_central_price_ratio_raw(
            prices_array=data_arrays.prices,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        central_price_macd_signal: arrays.ArrayFloat = raw.get_central_price_macd_raw(
            prices_array=data_arrays.prices,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=central_price_ratio_signal,
            indicator_signal=central_price_macd_signal,
        )


@_register_indicator
class MeanRateOfChangeMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        mean_roc_trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        mean_roc_macd_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
            len_macd=len_macd,
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=mean_roc_trend_signal,
            indicator_signal=mean_roc_macd_signal,
        )


@_register_indicator
class MedianRateOfChangeMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        median_roc_trend_signal: arrays.ArrayFloat = raw.get_median_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        median_roc_macd_signal: arrays.ArrayFloat = (
            raw.get_median_rate_of_change_macd_raw(
                returns_array=data_arrays.log_returns,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=median_roc_trend_signal,
            indicator_signal=median_roc_macd_signal,
        )


@_register_indicator
class CentralRateOfChangeMacdTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_st: int,
        len_lt: int,
        len_macd: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        central_roc_trend_signal: arrays.ArrayFloat = (
            raw.get_central_rate_of_change_raw(
                log_returns_array=data_arrays.log_returns,
                len_st=len_trend_st,
                len_lt=len_trend_lt,
            )
        )
        central_roc_macd_signal: arrays.ArrayFloat = (
            raw.get_central_rate_of_change_macd_raw(
                returns_array=data_arrays.log_returns,
                len_st=len_st,
                len_lt=len_lt,
                len_macd=len_macd,
            )
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=central_roc_trend_signal,
            indicator_signal=central_roc_macd_signal,
        )


@_register_indicator
class FixedBias(BaseIndic):
    def execute(self, data_arrays: AssetsData, Bias: int) -> arrays.ArrayFloat:
        return raw.get_fixed_bias(prices_array=data_arrays.prices, Bias=Bias)


@_register_indicator
class MeanPriceRatioNormalised(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_signal: int, len_norm: int
    ) -> arrays.ArrayFloat:
        normalised_price_ratio: arrays.ArrayFloat = (
            raw.get_normalised_mean_price_ratio_raw(
                prices_array=data_arrays.prices,
                len_signal=len_signal,
                len_norm=len_norm,
            )
        )
        return mt.limit_normalization(signal_array=normalised_price_ratio)


@_register_indicator
class MeanRateOfChangeNormalised(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_signal: int, len_norm: int
    ) -> arrays.ArrayFloat:
        normalised_roc: arrays.ArrayFloat = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_signal=len_signal,
            len_norm=len_norm,
        )

        return mt.limit_normalization(signal_array=normalised_roc)


@_register_indicator
class MeanRateOfChangeNormalisedTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_signal: int,
        len_norm: int,
        len_st: int,
        len_lt: int,
    ) -> arrays.ArrayFloat:
        normalised_roc: arrays.ArrayFloat = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_signal=len_signal,
            len_norm=len_norm,
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
        )
        normalised_on_trend_signal: arrays.ArrayFloat = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=normalised_roc
            )
        )
        return mt.limit_normalization(signal_array=normalised_on_trend_signal)


@_register_indicator
class MeanPriceRatioNormalisedTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_signal: int,
        len_norm: int,
        len_st: int,
        len_lt: int,
    ) -> arrays.ArrayFloat:
        normalised_ratio: arrays.ArrayFloat = (
            raw.get_normalised_mean_rate_of_change_raw(
                log_returns_array=data_arrays.log_returns,
                len_signal=len_signal,
                len_norm=len_norm,
            )
        )
        trend_signal = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_st,
            len_lt=len_lt,
        )
        normalised_on_trend_signal: arrays.ArrayFloat = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=normalised_ratio
            )
        )
        return mt.limit_normalization(signal_array=normalised_on_trend_signal)


@_register_indicator
class Skewness(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_skew: int
    ) -> arrays.ArrayFloat:
        skewness_array: arrays.ArrayFloat = raw.smoothed_skewness(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        return mt.sign_normalization(signal_array=-skewness_array)


@_register_indicator
class RelativeSkewness(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_skew: int
    ) -> arrays.ArrayFloat:
        relative_skew: arrays.ArrayFloat = raw.get_relative_skewness(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        return mt.sign_normalization(signal_array=relative_skew)


@_register_indicator
class SkewnessOnKurtosis(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_skew: int
    ) -> arrays.ArrayFloat:
        skew_on_kurt_signal: arrays.ArrayFloat = raw.get_skew_on_kurtosis(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        return mt.sign_normalization(signal_array=skew_on_kurt_signal)


@_register_indicator
class RelativeSkewnessOnKurtosis(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_skew: int
    ) -> arrays.ArrayFloat:
        relative_skew_on_kurt_signal: arrays.ArrayFloat = (
            raw.get_relative_skew_on_kurtosis(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
        )
        return mt.sign_normalization(signal_array=relative_skew_on_kurt_signal)


@_register_indicator
class SkewnessTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_skew: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        skewness_signal: arrays.ArrayFloat = raw.smoothed_skewness(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        skew_on_trend_signal: arrays.ArrayFloat = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=skewness_signal
        )
        return mt.sign_normalization(signal_array=skew_on_trend_signal)


@_register_indicator
class RelativeSkewnessTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_skew: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        relative_skewness_signal: arrays.ArrayFloat = raw.get_relative_skewness(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        relative_skew_on_trend: arrays.ArrayFloat = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=relative_skewness_signal
        )

        return mt.sign_normalization(signal_array=relative_skew_on_trend)


@_register_indicator
class SkewnessOnKurtosisTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_skew: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        skew_on_kurt_signal: arrays.ArrayFloat = raw.get_skew_on_kurtosis(
            log_returns_array=data_arrays.log_returns,
            len_smooth=len_smooth,
            len_skew=len_skew,
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=skew_on_kurt_signal
        )


@_register_indicator
class RelativeSkewnessOnKurtosisTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_skew: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        relative_skew_on_kurt_signal: arrays.ArrayFloat = (
            raw.get_relative_skew_on_kurtosis(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_skew=len_skew,
            )
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        relative_skew_on_kurt_on_trend: arrays.ArrayFloat = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_skew_on_kurt_signal,
            )
        )

        return mt.limit_normalization(signal_array=relative_skew_on_kurt_on_trend)


@_register_indicator
class DirectionalVolatility(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_vol: int
    ) -> arrays.ArrayFloat:
        return raw.smoothed_directional_volatility(
            returns_array=data_arrays.log_returns,
            len_st=len_smooth,
            len_vol=len_vol,
        )


@_register_indicator
class RelativeDirectionalVolatility(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_relative: int,
        len_vol: int,
    ) -> arrays.ArrayFloat:
        relative_directional_vol_signal: arrays.ArrayFloat = (
            raw.relative_directional_volatility(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_vol=len_vol,
                len_relative=len_relative,
            )
        )
        return mt.sign_normalization(signal_array=relative_directional_vol_signal)


@_register_indicator
class NormalisedDirectionalVolatility(BaseIndic):
    def execute(
        self, data_arrays: AssetsData, len_smooth: int, len_norm: int, len_vol: int
    ) -> arrays.ArrayFloat:
        normalised_directional_vol: arrays.ArrayFloat = (
            raw.normalised_directional_volatility(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_vol=len_vol,
                len_norm=len_norm,
            )
        )

        return mt.limit_normalization(signal_array=normalised_directional_vol)


@_register_indicator
class RelativeDirectionalVolatilityTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_relative: int,
        len_vol: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        relative_directional_vol_signal: arrays.ArrayFloat = (
            raw.relative_directional_volatility(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_vol=len_vol,
                len_relative=len_relative,
            )
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )

        relative_directional_vol_on_trend: arrays.ArrayFloat = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_directional_vol_signal,
            )
        )
        return mt.limit_normalization(signal_array=relative_directional_vol_on_trend)


@_register_indicator
class NormalisedDirectionalVolatilityTrend(BaseIndic):
    def execute(
        self,
        data_arrays: AssetsData,
        len_smooth: int,
        len_norm: int,
        len_vol: int,
        len_trend_st: int,
        len_trend_lt: int,
    ) -> arrays.ArrayFloat:
        normalised_directional_vol: arrays.ArrayFloat = (
            raw.normalised_directional_volatility(
                log_returns_array=data_arrays.log_returns,
                len_smooth=len_smooth,
                len_vol=len_vol,
                len_norm=len_norm,
            )
        )
        trend_signal: arrays.ArrayFloat = raw.get_mean_rate_of_change_raw(
            log_returns_array=data_arrays.log_returns,
            len_st=len_trend_st,
            len_lt=len_trend_lt,
        )
        normalised_directional_vol_on_trend: arrays.ArrayFloat = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=normalised_directional_vol,
            )
        )
        return mt.limit_normalization(signal_array=normalised_directional_vol_on_trend)
