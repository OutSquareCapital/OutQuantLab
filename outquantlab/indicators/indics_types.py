from outquantlab.indicators.params_types import (
    Trend,
    SmoothedSignal,
    SmoothedSignalTrend,
    AccelerationTrend,
    Acceleration,
    VolatilityTrend,
    Volatility
)
from outquantlab.indicators.interfaces import BaseIndic

class IndicTrend(BaseIndic[Trend]):

    def _get_combo(self, combination: tuple[int, ...]) -> Trend:
        return Trend(values=combination)

class IndicAcceleration(BaseIndic[Acceleration]):

    def _get_combo(self, combination: tuple[int, ...]) -> Acceleration:
        return Acceleration(values=combination)
    

class IndicVolatility(BaseIndic[Volatility]):

    def _get_combo(self, combination: tuple[int, ...]) -> Volatility:
        return Volatility(values=combination)

class IndicSmoothedSignal(BaseIndic[SmoothedSignal]):

    def _get_combo(self, combination: tuple[int, ...]) -> SmoothedSignal:
        return SmoothedSignal(values=combination)

class IndicSmoothedSignalTrend(BaseIndic[SmoothedSignalTrend]):

    def _get_combo(self, combination: tuple[int, ...]) -> SmoothedSignalTrend:
        return SmoothedSignalTrend(values=combination)

class IndicAccelerationTrend(BaseIndic[AccelerationTrend]):

    def _get_combo(self, combination: tuple[int, ...]) -> AccelerationTrend:
        return AccelerationTrend(values=combination)

class IndicVolatilityTrend(BaseIndic[VolatilityTrend]):

    def _get_combo(self, combination: tuple[int, ...]) -> VolatilityTrend:
        return VolatilityTrend(values=combination)