import outquantlab.indicators.indics_raw as raw
import outquantlab.metrics as mt
from outquantlab.indicators.indics_types import (
    IndicAcceleration,
    IndicAccelerationTrend,
    IndicSmoothedSignal,
    IndicSmoothedSignalTrend,
    IndicTrend,
    IndicVolatility,
    IndicVolatilityTrend,
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
)
from outquantlab.structures import arrays

INDICATOR_REGISTRY: dict[str, type[GenericIndic]] = {}


def register_indicator(cls: type[GenericIndic]) -> type[GenericIndic]:
    INDICATOR_REGISTRY[cls.__name__] = cls
    return cls


@register_indicator
class MeanPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        mean_price_ratio_raw: arrays.Float2D = raw.get_mean_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=mean_price_ratio_raw)


@register_indicator
class MedianPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        median_price_ratio_raw: arrays.Float2D = raw.get_median_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=median_price_ratio_raw)


@register_indicator
class CentralPriceRatio(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        central_price_ratio_raw: arrays.Float2D = raw.get_central_price_ratio_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=central_price_ratio_raw)


@register_indicator
class MeanRateOfChange(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        mean_roc_raw: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=mean_roc_raw)


@register_indicator
class MedianRateOfChange(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        median_roc_raw: arrays.Float2D = raw.get_median_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=median_roc_raw)


@register_indicator
class CentralRateOfChange(IndicTrend):
    def execute(self, data: AssetsData, params: Trend) -> arrays.Float2D:
        central_roc_raw: arrays.Float2D = raw.get_central_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=central_roc_raw)


@register_indicator
class MeanPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        mean_price_ratio_macd_raw: arrays.Float2D = raw.get_mean_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=mean_price_ratio_macd_raw)


@register_indicator
class MedianPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        median_price_ratio_macd_raw: arrays.Float2D = raw.get_median_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=median_price_ratio_macd_raw)


@register_indicator
class CentralPriceMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        central_price_ratio_macd_raw: arrays.Float2D = raw.get_central_price_macd_raw(
            prices_array=data.prices,
            params=params,
        )
        return mt.sign_normalization(signal_array=central_price_ratio_macd_raw)


@register_indicator
class MeanRateOfChangeMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        mean_roc_macd_raw: arrays.Float2D = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=mean_roc_macd_raw)


@register_indicator
class MedianRateOfChangeMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        median_roc_macd_raw: arrays.Float2D = raw.get_median_rate_of_change_macd_raw(
            returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=median_roc_macd_raw)


@register_indicator
class CentralRateOfChangeMacd(IndicAcceleration):
    def execute(self, data: AssetsData, params: Acceleration) -> arrays.Float2D:
        central_roc_macd_raw: arrays.Float2D = raw.get_central_rate_of_change_macd_raw(
            returns_array=data.log_returns,
            params=params,
        )
        return mt.sign_normalization(signal_array=central_roc_macd_raw)


@register_indicator
class MeanPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        mean_price_ratio_signal: arrays.Float2D = raw.get_mean_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        mean_price_macd_signal: arrays.Float2D = raw.get_mean_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )

        return mt.get_indicator_on_trend_signal(
            trend_signal=mean_price_ratio_signal,
            indicator_signal=mean_price_macd_signal,
        )


@register_indicator
class MedianPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        median_price_ratio_signal: arrays.Float2D = raw.get_median_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        median_price_macd_signal: arrays.Float2D = raw.get_median_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=median_price_ratio_signal,
            indicator_signal=median_price_macd_signal,
        )


@register_indicator
class CentralPriceMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        central_price_ratio_signal: arrays.Float2D = raw.get_central_price_ratio_raw(
            prices_array=data.prices,
            params=params.filter,
        )
        central_price_macd_signal: arrays.Float2D = raw.get_central_price_macd_raw(
            prices_array=data.prices, params=params.macd
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=central_price_ratio_signal,
            indicator_signal=central_price_macd_signal,
        )


@register_indicator
class MeanRateOfChangeMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        mean_roc_trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        mean_roc_macd_signal: arrays.Float2D = raw.get_mean_rate_of_change_macd_raw(
            returns_array=data.log_returns, params=params.macd
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=mean_roc_trend_signal,
            indicator_signal=mean_roc_macd_signal,
        )


@register_indicator
class MedianRateOfChangeMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        median_roc_trend_signal: arrays.Float2D = raw.get_median_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        median_roc_macd_signal: arrays.Float2D = raw.get_median_rate_of_change_macd_raw(
            returns_array=data.log_returns, params=params.macd
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=median_roc_trend_signal,
            indicator_signal=median_roc_macd_signal,
        )


@register_indicator
class CentralRateOfChangeMacdTrend(IndicAccelerationTrend):
    def execute(self, data: AssetsData, params: AccelerationTrend) -> arrays.Float2D:
        central_roc_trend_signal: arrays.Float2D = raw.get_central_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        central_roc_macd_signal: arrays.Float2D = (
            raw.get_central_rate_of_change_macd_raw(
                returns_array=data.log_returns, params=params.macd
            )
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=central_roc_trend_signal,
            indicator_signal=central_roc_macd_signal,
        )


@register_indicator
class FixedBias(BaseIndic[Bias]):
    def execute(self, data: AssetsData, params: Bias) -> arrays.Float2D:
        return arrays.create_full_like(
            model=data.prices, fill_value=arrays.Float32(1.0)
        )

    def _get_combo(self, combination: tuple[int, ...]) -> Bias:
        return Bias(values=combination)


@register_indicator
class MeanPriceRatioNormalised(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        normalised_price_ratio: arrays.Float2D = (
            raw.get_normalised_mean_price_ratio_raw(
                prices_array=data.prices, params=params
            )
        )
        return mt.limit_normalization(signal_array=normalised_price_ratio)


@register_indicator
class MeanRateOfChangeNormalised(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        normalised_roc: arrays.Float2D = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params
        )

        return mt.limit_normalization(signal_array=normalised_roc)


@register_indicator
class MeanRateOfChangeNormalisedTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        normalised_roc: arrays.Float2D = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        normalised_on_trend_signal: arrays.Float2D = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=normalised_roc
        )
        return mt.limit_normalization(signal_array=normalised_on_trend_signal)


@register_indicator
class MeanPriceRatioNormalisedTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        normalised_ratio: arrays.Float2D = raw.get_normalised_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.trend
        )
        normalised_on_trend_signal: arrays.Float2D = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=normalised_ratio
        )
        return mt.limit_normalization(signal_array=normalised_on_trend_signal)


@register_indicator
class Skewness(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        skewness_array: arrays.Float2D = raw.smoothed_skewness(
            log_returns_array=data.log_returns, params=params
        )
        return mt.sign_normalization(signal_array=-skewness_array)


@register_indicator
class RelativeSkewness(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        relative_skew: arrays.Float2D = raw.get_relative_skewness(
            log_returns_array=data.log_returns, params=params
        )
        return mt.sign_normalization(signal_array=relative_skew)


@register_indicator
class SkewnessOnKurtosis(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        skew_on_kurt_signal: arrays.Float2D = raw.get_skew_on_kurtosis(
            log_returns_array=data.log_returns, params=params
        )
        return mt.sign_normalization(signal_array=skew_on_kurt_signal)


@register_indicator
class RelativeSkewnessOnKurtosis(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
        relative_skew_on_kurt_signal: arrays.Float2D = (
            raw.get_relative_skew_on_kurtosis(
                log_returns_array=data.log_returns,
                params=params,
            )
        )

        return mt.sign_normalization(signal_array=relative_skew_on_kurt_signal)


@register_indicator
class SkewnessTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        skewness_signal: arrays.Float2D = raw.smoothed_skewness(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.trend
        )
        skew_on_trend_signal: arrays.Float2D = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=skewness_signal
        )
        return mt.sign_normalization(signal_array=skew_on_trend_signal)


@register_indicator
class RelativeSkewnessTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        relative_skewness_signal: arrays.Float2D = raw.get_relative_skewness(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns, params=params.trend
        )
        relative_skew_on_trend: arrays.Float2D = mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=relative_skewness_signal
        )

        return mt.sign_normalization(signal_array=relative_skew_on_trend)


@register_indicator
class SkewnessOnKurtosisTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        skew_on_kurt_signal: arrays.Float2D = raw.get_skew_on_kurtosis(
            log_returns_array=data.log_returns, params=params.smoothed_signal
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        return mt.get_indicator_on_trend_signal(
            trend_signal=trend_signal, indicator_signal=skew_on_kurt_signal
        )


@register_indicator
class RelativeSkewnessOnKurtosisTrend(IndicSmoothedSignalTrend):
    def execute(
        self,
        data: AssetsData,
        params: SmoothedSignalTrend,
    ) -> arrays.Float2D:
        relative_skew_on_kurt_signal: arrays.Float2D = (
            raw.get_relative_skew_on_kurtosis(
                log_returns_array=data.log_returns, params=params.smoothed_signal
            )
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.trend,
        )
        relative_skew_on_kurt_on_trend: arrays.Float2D = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_skew_on_kurt_signal,
            )
        )

        return mt.limit_normalization(signal_array=relative_skew_on_kurt_on_trend)


@register_indicator
class DirectionalVolatility(IndicSmoothedSignal):
    def execute(self, data: AssetsData, params: SmoothedSignal) -> arrays.Float2D:
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
    ) -> arrays.Float2D:
        relative_directional_vol_signal: arrays.Float2D = (
            raw.relative_directional_volatility(
                log_returns_array=data.log_returns, params=params
            )
        )
        return mt.sign_normalization(signal_array=relative_directional_vol_signal)


@register_indicator
class NormalisedDirectionalVolatility(IndicVolatility):
    def execute(self, data: AssetsData, params: Volatility) -> arrays.Float2D:
        normalised_directional_vol: arrays.Float2D = (
            raw.normalised_directional_volatility(
                log_returns_array=data.log_returns,
                params=params,
            )
        )

        return mt.limit_normalization(signal_array=normalised_directional_vol)


@register_indicator
class RelativeDirectionalVolatilityTrend(IndicVolatilityTrend):
    def execute(
        self,
        data: AssetsData,
        params: VolatilityTrend,
    ) -> arrays.Float2D:
        relative_directional_vol_signal: arrays.Float2D = (
            raw.relative_directional_volatility(
                log_returns_array=data.log_returns, params=params.volatility
            )
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )

        relative_directional_vol_on_trend: arrays.Float2D = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=relative_directional_vol_signal,
            )
        )
        return mt.limit_normalization(signal_array=relative_directional_vol_on_trend)


@register_indicator
class NormalisedDirectionalVolatilityTrend(IndicVolatilityTrend):
    def execute(
        self,
        data: AssetsData,
        params: VolatilityTrend,
    ) -> arrays.Float2D:
        normalised_directional_vol: arrays.Float2D = (
            raw.normalised_directional_volatility(
                log_returns_array=data.log_returns,
                params=params.volatility,
            )
        )
        trend_signal: arrays.Float2D = raw.get_mean_rate_of_change_raw(
            log_returns_array=data.log_returns,
            params=params.filter,
        )
        normalised_directional_vol_on_trend: arrays.Float2D = (
            mt.get_indicator_on_trend_signal(
                trend_signal=trend_signal,
                indicator_signal=normalised_directional_vol,
            )
        )
        return mt.limit_normalization(signal_array=normalised_directional_vol_on_trend)
