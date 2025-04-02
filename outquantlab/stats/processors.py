from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from outquantlab.apis import send_data_to_server
from outquantlab.stats.graphs import (
    Bars,
    Curves,
    HeatMap,
    Histograms,
    Violins,
    LogCurves
)
from outquantlab.structures import (
    ArrayFloat,
    SeriesFloat,
    DatedDataFrameFloat,
    DefaultDataFrameFloat,
)

type DefinedFunc = Callable[[ArrayFloat], ArrayFloat]
type ParametrableFunc = Callable[[ArrayFloat, int], ArrayFloat]


@dataclass(slots=True)
class StatProcessor[
    D: DatedDataFrameFloat | SeriesFloat | DefaultDataFrameFloat,
    F: Callable[..., ArrayFloat],
](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def send_to_api(self, data: DatedDataFrameFloat, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_formatted_data(
        self, data: DatedDataFrameFloat, *args: Any, **kwargs: Any
    ) -> D:
        raise NotImplementedError


class EquityProcessor(StatProcessor[DatedDataFrameFloat, DefinedFunc]):
    def get_formatted_data(self, data: DatedDataFrameFloat) -> DatedDataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array())
        return DatedDataFrameFloat(
            data=stats_array,
            index=data.get_index(),
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def send_to_api(self, data: DatedDataFrameFloat) -> None:
        send_data_to_server(
            id=self._name,
            results=self.get_formatted_data(data=data).convert_to_json(),
        )

    def plot(self, data: DatedDataFrameFloat) -> None:
        LogCurves(
            formatted_data=self.get_formatted_data(data=data),
            title=self._name,
        )


class RollingProcessor(StatProcessor[DatedDataFrameFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: DatedDataFrameFloat, length: int
    ) -> DatedDataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array(), length)
        return DatedDataFrameFloat(
            data=stats_array,
            index=data.get_index(),
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def send_to_api(self, data: DatedDataFrameFloat, length: int) -> None:
        send_data_to_server(
            id=self._name,
            results=self.get_formatted_data(data=data, length=length).convert_to_json(),
        )

    def plot(self, data: DatedDataFrameFloat, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[DefaultDataFrameFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: DatedDataFrameFloat, frequency: int
    ) -> DefaultDataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array(), frequency)
        return DefaultDataFrameFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def send_to_api(self, data: DatedDataFrameFloat, frequency: int) -> None:
        send_data_to_server(
            id=self._name,
            results=self.get_formatted_data(
                data=data, frequency=frequency
            ).convert_to_json(),
        )

    def plot_violins(self, data: DatedDataFrameFloat, frequency: int) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(self, data: DatedDataFrameFloat, frequency: int) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[DefaultDataFrameFloat, DefinedFunc]):
    def get_formatted_data(self, data: DefaultDataFrameFloat) -> DefaultDataFrameFloat:
        stats_array: ArrayFloat = self._func(data.get_array())
        return DefaultDataFrameFloat(
            data=stats_array,
            columns=data.get_names(),
        )

    def send_to_api(self, data: DefaultDataFrameFloat) -> None:
        send_data_to_server(
            id=self._name, results=self.get_formatted_data(data=data).convert_to_json()
        )

    def plot(self, data: DefaultDataFrameFloat) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[SeriesFloat, DefinedFunc]):
    def get_formatted_data(self, data: DatedDataFrameFloat) -> SeriesFloat:
        stats_array: ArrayFloat = self._func(data.get_array())
        return SeriesFloat(data=stats_array, index=data.get_names()).sort_data(
            ascending=self._ascending
        )

    def send_to_api(self, data: DatedDataFrameFloat) -> None:
        send_data_to_server(
            id=self._name, results=self.get_formatted_data(data=data).convert_to_json()
        )

    def plot(self, data: DatedDataFrameFloat) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
