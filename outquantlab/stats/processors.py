from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from outquantlab.stats.graphs import (
    Bars,
    Curves,
    HeatMap,
    Histograms,
    Violins,
)
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat

type DefinedFunc = Callable[[ArrayFloat], ArrayFloat]
type ParametrableFunc = Callable[[ArrayFloat, int], ArrayFloat]


@dataclass(slots=True)
class StatProcessor[D: DataFrameFloat | SeriesFloat, F: Callable[..., ArrayFloat]](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def get_formatted_data(self, data: DataFrameFloat, *args: Any, **kwargs: Any) -> D:
        raise NotImplementedError

    @abstractmethod
    def get_serialized_data(
        self, data: DataFrameFloat, *args: Any, **kwargs: Any
    ) -> dict[str, dict[str, list[str]]]:
        raise NotImplementedError


class RollingProcessor(StatProcessor[DataFrameFloat, ParametrableFunc]):
    def get_formatted_data(self, data: DataFrameFloat, length: int) -> DataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array(), length)
        return DataFrameFloat(
            data=stats_array,
            index=data.dates,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def get_serialized_data(
        self, data: DataFrameFloat, length: int
    ) -> dict[str, dict[str, list[str]]]:
        return self.get_formatted_data(data=data, length=length).convert_to_json(
            title=self._name
        )

    def plot(self, data: DataFrameFloat, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[DataFrameFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: DataFrameFloat, frequency: int
    ) -> DataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array(), frequency)
        return DataFrameFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def get_serialized_data(
        self, data: DataFrameFloat, frequency: int
    ) -> dict[str, dict[str, list[str]]]:
        return self.get_formatted_data(data=data, frequency=frequency).convert_to_json(
            title=self._name
        )

    def plot_violins(self, data: DataFrameFloat, frequency: int) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(self, data: DataFrameFloat, frequency: int) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[DataFrameFloat, DefinedFunc]):
    def get_formatted_data(self, data: DataFrameFloat) -> DataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array())
        return DataFrameFloat(
            data=stats_array,
            columns=data.get_names(),
        )

    def get_serialized_data(
        self, data: DataFrameFloat
    ) -> dict[str, dict[str, list[str]]]:
        return self.get_formatted_data(data=data).convert_to_json(title=self._name)

    def plot(self, data: DataFrameFloat) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[SeriesFloat, DefinedFunc]):
    def get_formatted_data(self, data: DataFrameFloat) -> SeriesFloat:
        stats_array: ArrayFloat = self._func(data.get_array())
        return SeriesFloat(data=stats_array, index=data.get_names()).sort_data(
            ascending=self._ascending
        )

    def get_serialized_data(
        self, data: DataFrameFloat
    ) -> dict[str, dict[str, list[str]]]:
        return self.get_formatted_data(data=data).convert_to_json(title=self._name)

    def plot(self, data: DataFrameFloat) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
