from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias, TypeVar
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat

StatSerieInterface: TypeAlias = Callable[[DataFrameFloat], SeriesFloat]
StatDataFrameInterface: TypeAlias = Callable[[DataFrameFloat, int], DataFrameFloat]
T = TypeVar("T", bound=DataFrameFloat | SeriesFloat)


@dataclass
class DataProcessorDF:
    func: StatDataFrameInterface

    def process(self, data: DataFrameFloat, length: int) -> DataFrameFloat:
        return self.func(data, length)

    @property
    def title(self) -> str:
        return self.func.__name__.replace("get", "").replace("_", " ").title()


@dataclass
class DataProcessorSeries:
    func: StatSerieInterface

    def process(self, data: DataFrameFloat) -> SeriesFloat:
        return self.func(data)

    @property
    def title(self) -> str:
        return self.func.__name__.replace("get", "").replace("_", " ").title()
