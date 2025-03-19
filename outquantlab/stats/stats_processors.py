from collections.abc import Callable
from typing import TypeAlias
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

ParametrableMetric: TypeAlias = Callable[[ArrayFloat, int], ArrayFloat]
AggregateMetric: TypeAlias = Callable[[ArrayFloat], ArrayFloat]
OverallMetrics: TypeAlias = list[AggregateMetric]


def _format_name(name: str) -> str:
    return name.replace("get", "").replace("_", " ").title()


class StatsOverall:
    def __init__(self, data: DataFrameFloat, overall_metrics: OverallMetrics) -> None:
        self.metrics_func: OverallMetrics = overall_metrics
        self.data: SeriesFloat = self.get_data(returns_df=data)
        self.title: str = "Overall Stats"

    def get_data(self, returns_df: DataFrameFloat) -> SeriesFloat:
        array: ArrayFloat = returns_df.get_array()
        results: list[ArrayFloat] = [func(array) for func in self.metrics_func]
        names: list[str] = [
            _format_name(name=func.__name__) for func in self.metrics_func
        ]
        results_list: list[float] = [result.item() for result in results]
        return SeriesFloat.from_float_list(data=results_list, index=names)


class StatsCurves:
    def __init__(
        self,
        data: DataFrameFloat,
        func: ParametrableMetric,
        ascending: bool,
        length: int,
    ) -> None:
        self.func: ParametrableMetric = func
        self.data: DataFrameFloat = self.get_data(
            data=data, ascending=ascending, length=length
        )
        self.title: str = _format_name(name=self.func.__name__)

    def get_data(
        self, data: DataFrameFloat, ascending: bool, length: int
    ) -> DataFrameFloat:
        array: ArrayFloat = self.func(data.get_array(), length)
        return DataFrameFloat(
            data=array,
            index=data.dates,
            columns=data.get_names(),
        ).sort_data(ascending=ascending)


class StatsDistribution:
    def __init__(
        self,
        data: DataFrameFloat,
        func: ParametrableMetric,
        ascending: bool,
        frequency: int,
    ) -> None:
        self.func: ParametrableMetric = func
        self.data: DataFrameFloat = self.get_data(
            data=data, ascending=ascending, frequency=frequency
        )
        self.title: str = _format_name(name=self.func.__name__)

    def get_data(
        self, data: DataFrameFloat, ascending: bool, frequency: int
    ) -> DataFrameFloat:
        array: ArrayFloat = self.func(data.get_array(), frequency)
        return DataFrameFloat(
            data=array,
            columns=data.get_names(),
        ).sort_data(ascending=ascending)


class StatsBars:
    def __init__(
        self,
        data: DataFrameFloat,
        func: AggregateMetric,
        ascending: bool,
    ) -> None:
        self.func: AggregateMetric = func
        self.data: SeriesFloat = self.get_data(data=data, ascending=ascending)
        self.title: str = _format_name(name=self.func.__name__)

    def get_data(self, data: DataFrameFloat, ascending: bool) -> SeriesFloat:
        array: ArrayFloat = self.func(data.get_array())
        return SeriesFloat(data=array, index=data.get_names()).sort_data(
            ascending=ascending
        )


class StatsHeatMap:
    def __init__(self, data: DataFrameFloat, func: AggregateMetric) -> None:
        self.func: AggregateMetric = func
        self.data: DataFrameFloat = self.get_data(data=data)
        self.title: str = "Correlation Matrix"

    def get_data(self, data: DataFrameFloat) -> DataFrameFloat:
        array: ArrayFloat = self.func(data.get_array())
        return DataFrameFloat(
            data=array,
            columns=data.get_names(),
        )
