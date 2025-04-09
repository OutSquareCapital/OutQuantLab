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
from outquantlab.structures import arrays, frames

type DefinedFunc = Callable[[arrays.Float2D], arrays.Float2D]
type ParametrableFunc = Callable[[arrays.Float2D, int], arrays.Float2D]
type OptionalFunc = Callable[[arrays.Float2D, int | None], arrays.Float2D]


@dataclass(slots=True)
class StatProcessor[
    D: frames.DatedFloat | frames.SeriesFloat | frames.DefaultFloat,
    F: Callable[..., arrays.Float2D],
](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def get_formatted_data(
        self, data: frames.DatedFloat, *args: Any, **kwargs: Any
    ) -> D:
        raise NotImplementedError


class EquityProcessor(StatProcessor[frames.DefaultFloat, OptionalFunc]):
    def get_formatted_data(
        self, data: frames.DatedFloat, frequency: int | None = None
    ) -> frames.DefaultFloat:
        stats_array: arrays.Float2D = self._func(data.get_array(), frequency)
        return frames.DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: frames.DatedFloat, frequency: int | None = None) -> None:
        LogCurves(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class RollingProcessor(StatProcessor[frames.DatedFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: frames.DatedFloat, length: int
    ) -> frames.DatedFloat:
        stats_array: arrays.Float2D = self._func(data.get_array(), length)
        return frames.DatedFloat(
            data=stats_array,
            index=data.get_index(),
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: frames.DatedFloat, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[frames.DefaultFloat, ParametrableFunc]):
    def get_formatted_data(
        self, data: frames.DatedFloat, frequency: int
    ) -> frames.DefaultFloat:
        stats_array: arrays.Float2D = self._func(data.get_array(), frequency)
        return frames.DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot_violins(self, data: frames.DatedFloat, frequency: int) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(self, data: frames.DatedFloat, frequency: int) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_boxes(self, data: frames.DatedFloat, frequency: int) -> None:
        Boxes(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[frames.DefaultFloat, DefinedFunc]):
    def get_formatted_data(self, data: frames.DefaultFloat) -> frames.DefaultFloat:
        stats_array: arrays.Float2D = self._func(data.get_array())
        return frames.DefaultFloat(
            data=stats_array,
            columns=data.get_names(),
        )

    def plot(self, data: frames.DefaultFloat) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[frames.SeriesFloat, DefinedFunc]):
    def get_formatted_data(self, data: frames.DatedFloat) -> frames.SeriesFloat:
        stats_array: arrays.Float2D = self._func(data.get_array())
        return frames.SeriesFloat(data=stats_array, index=data.get_names()).sort_data(
            ascending=self._ascending
        )

    def plot(self, data: frames.DatedFloat) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
