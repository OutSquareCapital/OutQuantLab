import numquant as nq
import outquantlab.indicators.indics_raw as raw
from outquantlab.indicators.indics_types import (
    IndicAcceleration,
    IndicAccelerationTrend,
    IndicSmoothedSignal,
    IndicSmoothedSignalTrend,
    IndicTrend,
    IndicVolatility,
    IndicVolatilityTrend,
    IndicNormalizedSmoothedSignal,
    IndicNormalizedSmoothedSignalTrend
)
from outquantlab.indicators.interfaces import AssetsData, BaseIndic, GenericIndic
from outquantlab.indicators.params_types import (
    Acceleration,
    AccelerationTrend,
    Bias,
    SmoothedSignal,
    SmoothedSignalTrend,
    Trend,
    Volatility,
    VolatilityTrend,
    NormalizedSmoothedSignal,
    NormalizedSmoothedSignalTrend,
)

INDICATOR_REGISTRY: dict[str, type[GenericIndic]] = {}


def register_indicator(cls: type[GenericIndic]) -> type[GenericIndic]:
    INDICATOR_REGISTRY[cls.__name__] = cls
    return cls


@register_indicator
class MeanPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> nq.Float2D:
        mean_price_ratio_raw: nq.Float2D = raw.get_mean_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=mean_price_ratio_raw)


@register_indicator
class MedianPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> nq.Float2D:
        median_price_ratio_raw: nq.Float2D = raw.get_median_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=median_price_ratio_raw)


@register_indicator
class CentralPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> nq.Float2D:
        central_price_ratio_raw: nq.Float2D = raw.get_central_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=central_price_ratio_raw)


@register_indicator
class MeanRateOfChange(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> nq.Float2D:
        mean_roc_raw: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=mean_roc_raw)


@register_indicator
class MedianRateOfChange(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> nq.Float2D:
        median_roc_raw: nq.Float2D = raw.get_median_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=median_roc_raw)


@register_indicator
class MeanPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> nq.Float2D:
        mean_price_ratio_macd_raw: nq.Float2D = raw.get_mean_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(
            signal_array=mean_price_ratio_macd_raw
        )


@register_indicator
class MedianPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> nq.Float2D:
        median_price_ratio_macd_raw: nq.Float2D = raw.get_median_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(
            signal_array=median_price_ratio_macd_raw
        )


@register_indicator
class CentralPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> nq.Float2D:
        central_price_ratio_macd_raw: nq.Float2D = raw.get_central_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(
            signal_array=central_price_ratio_macd_raw
        )


@register_indicator
class MeanRateOfChangeMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> nq.Float2D:
        mean_roc_macd_raw: nq.Float2D = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data.log_returns,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=mean_roc_macd_raw)


@register_indicator
class MedianRateOfChangeMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> nq.Float2D:
        median_roc_macd_raw: nq.Float2D = raw.get_median_rate_of_change_macd_raw(
            returns_array=data.log_returns,
            params=params,
        )
        return nq.metrics.roll.sign_normalization(signal_array=median_roc_macd_raw)


@register_indicator
class MeanPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> nq.Float2D:
        mean_price_ratio_signal: nq.Float2D = raw.get_mean_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        mean_price_macd_signal: nq.Float2D = raw.get_mean_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )

        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=mean_price_ratio_signal,
            indicator_signal=mean_price_macd_signal,
        )


@register_indicator
class MedianPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> nq.Float2D:
        median_price_ratio_signal: nq.Float2D = raw.get_median_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        median_price_macd_signal: nq.Float2D = raw.get_median_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )
        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=median_price_ratio_signal,
            indicator_signal=median_price_macd_signal,
        )


@register_indicator
class CentralPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> nq.Float2D:
        central_price_ratio_signal: nq.Float2D = raw.get_central_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        central_price_macd_signal: nq.Float2D = raw.get_central_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )
        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=central_price_ratio_signal,
            indicator_signal=central_price_macd_signal,
        )


@register_indicator
class MeanRateOfChangeMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> nq.Float2D:
        mean_roc_trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        mean_roc_macd_signal: nq.Float2D = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data.log_returns, params=params.macd
        )
        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=mean_roc_trend_signal,
            indicator_signal=mean_roc_macd_signal,
        )


@register_indicator
class MedianRateOfChangeMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> nq.Float2D:
        median_roc_trend_signal: nq.Float2D = raw.get_median_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        median_roc_macd_signal: nq.Float2D = raw.get_median_rate_of_change_macd_raw(
            returns_array=data.log_returns, params=params.macd
        )
        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=median_roc_trend_signal,
            indicator_signal=median_roc_macd_signal,
        )


@register_indicator
class FixedBias(BaseIndic[Bias]):
    def execute(self, data: AssetsData, params: Bias) -> nq.Float2D:
        return nq.arrays.create_full_like(model=data.prices, fill_value=nq.Float32(1.0))

    def _get_combo(self, combination: tuple[int, ...]) -> Bias:
        return Bias(values=combination)


@register_indicator
class MeanPriceRatioNormalised(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> nq.Float2D:
        normalised_price_ratio: nq.Float2D = raw.get_normalised_mean_price_ratio_raw(
            prices_array=data.prices, params=params
        )
        return nq.metrics.roll.limit_normalization(signal_array=normalised_price_ratio)


@register_indicator
class MeanRateOfChangeNormalised(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> nq.Float2D:
        normalised_roc: nq.Float2D = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params
        )

        return nq.metrics.roll.limit_normalization(signal_array=normalised_roc)


@register_indicator
class MeanRateOfChangeNormalisedTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> nq.Float2D:
        normalised_roc: nq.Float2D = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        normalised_on_trend_signal: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=normalised_roc
            )
        )
        return nq.metrics.roll.limit_normalization(
            signal_array=normalised_on_trend_signal
        )


@register_indicator
class MeanPriceRatioNormalisedTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> nq.Float2D:
        normalised_ratio: nq.Float2D = raw.get_normalised_mean_price_ratio_raw(
            prices_array=data.prices, params=params.smoothed_signal
        )
        trend_signal: nq.Float2D = raw.get_mean_price_ratio_raw(
            prices_array=data.prices, params=params.trend
        )
        normalised_on_trend_signal: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=normalised_ratio
            )
        )
        return nq.metrics.roll.limit_normalization(
            signal_array=normalised_on_trend_signal
        )


@register_indicator
class Skewness(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> nq.Float2D:
        skewness_array: nq.Float2D = raw.smoothed_skewness(
            log_returns_array=data.log_returns, params=params
        )
        return nq.metrics.roll.sign_normalization(signal_array=-skewness_array)


@register_indicator
class RelativeSkewness(IndicNormalizedSmoothedSignal):
    def execute(self, data: AssetsData, params: NormalizedSmoothedSignal) -> nq.Float2D:
        relative_skew: nq.Float2D = raw.get_relative_skewness(
            log_returns_array=data.log_returns, params=params
        )
        return nq.metrics.roll.sign_normalization(signal_array=relative_skew)


@register_indicator
class SkewnessOnKurtosis(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> nq.Float2D:
        skew_on_kurt_signal: nq.Float2D = raw.get_skew_on_kurtosis(
            log_returns_array=data.log_returns, params=params
        )
        return nq.metrics.roll.sign_normalization(signal_array=skew_on_kurt_signal)


@register_indicator
class RelativeSkewnessOnKurtosis(IndicNormalizedSmoothedSignal):
    def execute(self, data: AssetsData, params: NormalizedSmoothedSignal) -> nq.Float2D:
        relative_skew_on_kurt_signal: nq.Float2D = raw.get_relative_skew_on_kurtosis(
            log_returns_array=data.log_returns,
            params=params,
        )

        return nq.metrics.roll.sign_normalization(
            signal_array=relative_skew_on_kurt_signal
        )


@register_indicator
class SkewnessTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> nq.Float2D:
        skewness_signal: nq.Float2D = raw.smoothed_skewness(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.trend
        )
        skew_on_trend_signal: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=skewness_signal
            )
        )
        return nq.metrics.roll.sign_normalization(signal_array=skew_on_trend_signal)


@register_indicator
class RelativeSkewnessTrend(IndicNormalizedSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: NormalizedSmoothedSignalTrend,
    ) -> nq.Float2D:
        relative_skewness_signal: nq.Float2D = raw.get_relative_skewness(
            log_returns_array=data.log_returns, params=params.signal
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.trend
        )
        relative_skew_on_trend: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal, indicator_signal=relative_skewness_signal
            )
        )

        return nq.metrics.roll.sign_normalization(signal_array=relative_skew_on_trend)


@register_indicator
class SkewnessOnKurtosisTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> nq.Float2D:
        skew_on_kurt_signal: nq.Float2D = raw.get_skew_on_kurtosis(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        return nq.metrics.roll.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=skew_on_kurt_signal
        )


@register_indicator
class RelativeSkewnessOnKurtosisTrend(IndicNormalizedSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: NormalizedSmoothedSignalTrend,
    ) -> nq.Float2D:
        relative_skew_on_kurt_signal: nq.Float2D = raw.get_relative_skew_on_kurtosis(
            log_returns_array=data.log_returns, params=params.signal
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        relative_skew_on_kurt_on_trend: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_skew_on_kurt_signal,
            )
        )

        return nq.metrics.roll.limit_normalization(
            signal_array=relative_skew_on_kurt_on_trend
        )


@register_indicator
class DirectionalVolatility(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> nq.Float2D:
        return raw.smoothed_directional_volatility(
            returns_array=data.log_returns,
            params=params,
        )


@register_indicator
class RelativeDirectionalVolatility(IndicVolatility):
    def execute(
        self,
        data: AssetsData,
        params: Volatility,
    ) -> nq.Float2D:
        relative_directional_vol_signal: nq.Float2D = (
            raw.relative_directional_volatility(
                log_returns_array=data.log_returns, params=params
            )
        )
        return nq.metrics.roll.sign_normalization(
            signal_array=relative_directional_vol_signal
        )


@register_indicator
class NormalisedDirectionalVolatility(IndicVolatility):
    def execute(self, data: AssetsData, params: Volatility) -> nq.Float2D:
        normalised_directional_vol: nq.Float2D = raw.normalised_directional_volatility(
            log_returns_array=data.log_returns,
            params=params,
        )

        return nq.metrics.roll.limit_normalization(
            signal_array=normalised_directional_vol
        )


@register_indicator
class RelativeDirectionalVolatilityTrend(IndicVolatilityTrend):
    def execute(
        self,
        data: AssetsData,
        params: VolatilityTrend,
    ) -> nq.Float2D:
        relative_directional_vol_signal: nq.Float2D = (
            raw.relative_directional_volatility(
                log_returns_array=data.log_returns, params=params.volatility
            )
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )

        relative_directional_vol_on_trend: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_directional_vol_signal,
            )
        )
        return nq.metrics.roll.limit_normalization(
            signal_array=relative_directional_vol_on_trend
        )


@register_indicator
class NormalisedDirectionalVolatilityTrend(IndicVolatilityTrend):
    def execute(
        self,
        data: AssetsData,
        params: VolatilityTrend,
    ) -> nq.Float2D:
        normalised_directional_vol: nq.Float2D = raw.normalised_directional_volatility(
            log_returns_array=data.log_returns,
            params=params.volatility,
        )
        trend_signal: nq.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        normalised_directional_vol_on_trend: nq.Float2D = (
            nq.metrics.roll.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=normalised_directional_vol,
            )
        )
        return nq.metrics.roll.limit_normalization(
            signal_array=normalised_directional_vol_on_trend
        )
