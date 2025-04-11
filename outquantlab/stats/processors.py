from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from outquantlab.stats.graphs import (
    Bars,
    Boxes,
    Curves,
    HeatMap,
    Histograms,
    LogCurves,
    Violins,
)
import numquant as nq 
from outquantlab.frames import SeriesFloat, DefaultFloat, DatedFloat

type DefinedFunc = Callable[[nq.Float2D], nq.Float2D]
type ParametrableFunc = Callable[[nq.Float2D, int], nq.Float2D]
type OptionalFunc = Callable[[nq.Float2D, int | None], nq.Float2D]


@dataclass(slots=True)
class StatProcessor[
    D: DatedFloat | SeriesFloat | DefaultFloat,
    F: Callable[..., nq.Float2D],
](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def get_formatted_data(
        self, data: DatedFloat, *args: Any, **kwargs: Any
    ) -> D:
        raise NotImplementedError


class EquityProcessor(StatProcessor[DefaultFloat, OptionalFunc]):
    def get_formatted_data(
        self, data: DatedFloat, frequency: int | None = None
    ) -> DefaultFloat:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: DatedFloat, frequency: int | None = None) -> None:
        LogCurves(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class RollingProcessor(StatProcessor[DatedFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: DatedFloat, length: int
    ) -> DatedFloat:
        stats_array: nq.Float2D = self._func(data.get_array(), length)
        return DatedFloat(
            data=stats_array,
            index=data.get_index(),
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: DatedFloat, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[DefaultFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: DatedFloat, frequency: int
    ) -> DefaultFloat:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot_violins(self, data: DatedFloat, frequency: int) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(self, data: DatedFloat, frequency: int) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_boxes(self, data: DatedFloat, frequency: int) -> None:
        Boxes(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[DefaultFloat, DefinedFunc]):
    def get_formatted_data(self, data: DefaultFloat) -> DefaultFloat:
        stats_array: nq.Float2D = self._func(data.get_array())
        return DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        )

    def plot(self, data: DefaultFloat) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[SeriesFloat, DefinedFunc]):
    def get_formatted_data(self, data: DatedFloat) -> SeriesFloat:
        stats_array: nq.Float2D = self._func(data.get_array())
        return SeriesFloat(data=stats_array, index=data.get_names()).sort_data(
            ascending=self._ascending
        )

    def plot(self, data: DatedFloat) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
