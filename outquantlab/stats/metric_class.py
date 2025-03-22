from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat
from collections.abc import Callable
from typing import Generic, TypeVar, TypeAlias, Any
from abc import ABC, abstractmethod

ParametrableFunc: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
DefinedFunc: TypeAlias = Callable[[ArrayFloat], ArrayFloat]
OverallFuncs: TypeAlias = list[DefinedFunc]

T = TypeVar("T", bound=ParametrableFunc | DefinedFunc)
D = TypeVar("D", bound=DataFrameFloat | SeriesFloat)


class Metric(ABC, Generic[T, D]):
    def __init__(self, func: T, ascending: bool) -> None:
        self._func: T = func
        self._ascending: bool = ascending
        self.title: str = _format_name(name=func.__name__)

    @abstractmethod
    def get_data(self, *args: Any, **kwargs: Any) -> D: ...


class CurvesMetric(Metric[ParametrableFunc, DataFrameFloat]):
    def get_data(
        self,
        returns_df: DataFrameFloat,
        length: int,
    ) -> DataFrameFloat:
        array: ArrayFloat = self._func(returns_df.get_array(), length)
        return DataFrameFloat(
            data=array,
            index=returns_df.dates,
            columns=returns_df.get_names(),
        ).sort_data(ascending=self._ascending)


class HistogramMetric(Metric[ParametrableFunc, DataFrameFloat]):
    def get_data(
        self,
        returns_df: DataFrameFloat,
        frequency: int,
    ) -> DataFrameFloat:
        array: ArrayFloat = self._func(returns_df.get_array(), frequency)
        return DataFrameFloat(
            data=array,
            columns=returns_df.get_names(),
        ).sort_data(ascending=self._ascending)


class BarsMetric(Metric[DefinedFunc, SeriesFloat]):
    def get_data(self, returns_df: DataFrameFloat) -> SeriesFloat:
        array: ArrayFloat = self._func(returns_df.get_array())
        return SeriesFloat(data=array, index=returns_df.get_names()).sort_data(
            ascending=self._ascending
        )


class HeatMapMetric(Metric[DefinedFunc, DataFrameFloat]):
    def get_data(self, returns_df: DataFrameFloat) -> DataFrameFloat:
        array: ArrayFloat = self._func(returns_df.get_array())
        return DataFrameFloat(
            data=array,
            columns=returns_df.get_names(),
        )


class OverallMetrics:
    def __init__(self, overall_metrics: OverallFuncs) -> None:
        self._overall_metrics: OverallFuncs = overall_metrics
        self.title: str = "Overall Metrics"

    def _get_names(self) -> list[str]:
        return [_format_name(name=func.__name__) for func in self._overall_metrics]

    def get_data(self, returns_df: DataFrameFloat) -> SeriesFloat:
        array: ArrayFloat = returns_df.get_array()
        names: list[str] = self._get_names()
        raw_results: list[ArrayFloat] = [func(array) for func in self._overall_metrics]
        results_list: list[float] = [result.item() for result in raw_results]
        return SeriesFloat.from_float_list(data=results_list, index=names)

def _format_name(name: str) -> str:
    return name.replace("get", "").replace("_", " ").title()
