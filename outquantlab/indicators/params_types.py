from dataclasses import dataclass, field

from outquantlab.indicators.interfaces import BaseParams


@dataclass(slots=True)
class Trend(BaseParams):
    short: int = field(init=False)
    long: int = field(init=False)

    def __post_init__(self) -> None:
        self.short = self.values[0]
        self.long = self.values[1]

    def validate(self) -> bool:
        return self.short * 4 <= self.long


@dataclass(slots=True)
class SmoothedSignal(BaseParams):
    smoothing: int = field(init=False)
    signal: int = field(init=False)

    def __post_init__(self) -> None:
        self.smoothing = self.values[0]
        self.signal = self.values[1]

    def validate(self) -> bool:
        return self.smoothing > 1


@dataclass(slots=True)
class SmoothedSignalTrend(BaseParams):
    trend: Trend = field(init=False)
    smoothed_signal: SmoothedSignal = field(init=False)

    def __post_init__(self) -> None:
        self.trend = Trend(values=self.values[:2])
        self.smoothed_signal = SmoothedSignal(values=self.values[2:4])

    def validate(self) -> bool:
        return self.trend.validate() and self.smoothed_signal.validate()


@dataclass(slots=True)
class Acceleration(BaseParams):
    trend: Trend = field(init=False)
    acceleration: int = field(init=False)

    def __post_init__(self) -> None:
        self.trend = Trend(values=self.values[:2])
        self.acceleration = self.values[2]

    def validate(self) -> bool:
        return self.trend.validate() and self.acceleration < 64


@dataclass(slots=True)
class AccelerationTrend(BaseParams):
    filter: Trend = field(init=False)
    macd: Acceleration = field(init=False)

    def __post_init__(self) -> None:
        self.filter = Trend(values=self.values[:2])
        self.macd = Acceleration(values=self.values[2:5])

    def validate(self) -> bool:
        return self.filter.validate() and self.macd.validate()


@dataclass(slots=True)
class Volatility(BaseParams):
    smoothed_signal: SmoothedSignal = field(init=False)
    normalization: int = field(init=False)

    def __post_init__(self) -> None:
        self.smoothed_signal = SmoothedSignal(values=self.values[:2])
        self.normalization = self.values[2]

    def validate(self) -> bool:
        return (
            self.smoothed_signal.validate()
            and self.normalization > self.smoothed_signal.smoothing
        )


@dataclass(slots=True)
class VolatilityTrend(BaseParams):
    filter: Trend = field(init=False)
    volatility: Volatility = field(init=False)

    def __post_init__(self) -> None:
        self.filter = Trend(values=self.values[:2])
        self.volatility = Volatility(values=self.values[2:5])

    def validate(self) -> bool:
        return self.filter.validate() and self.volatility.validate()


@dataclass(slots=True)
class Bias(BaseParams):
    bias: int = field(init=False)

    def __post_init__(self) -> None:
        self.bias = self.values[0]

    def validate(self) -> bool:
        return True
