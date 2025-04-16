from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import numquant as nq
import tradeframe as tf
from outquantlab.stats.graphs import (
    Bars,
    Boxes,
    Curves,
    HeatMap,
    Histograms,
    LogCurves,
    Violins,
)

type DefinedFunc = Callable[[nq.Float2D], nq.Float2D]
type ParametrableFunc = Callable[[nq.Float2D, int], nq.Float2D]
type OptionalFunc = Callable[[nq.Float2D, int | None], nq.Float2D]


@dataclass(slots=True)
class StatProcessor[
    D: tf.FrameDated
    | tf.FrameDefault
    | tf.SeriesNamed
    | tf.SeriesDefault
    | tf.FrameMatrix,
    F: Callable[..., nq.Float2D],
](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def get_formatted_data(self, data: tf.FrameDated, *args: Any, **kwargs: Any) -> D:
        raise NotImplementedError


class EquityProcessor(StatProcessor[tf.FrameDefault, OptionalFunc]):
    def get_formatted_data(
        self, data: tf.FrameDated, frequency: int | None = None
    ) -> tf.FrameDefault:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: tf.FrameDated, frequency: int | None = None) -> None:
        LogCurves(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class RollingProcessor(StatProcessor[tf.FrameDated, ParametrableFunc]):
    def get_formatted_data(self, data: tf.FrameDated, length: int) -> tf.FrameDated:
        stats_array: nq.Float2D = self._func(data.get_array(), length)

        return tf.FrameDated.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
            dates=data.index,
        ).sort_data(ascending=self._ascending)

    def plot(self, data: tf.FrameDated, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[tf.FrameDefault, OptionalFunc]):
    def get_formatted_data(
        self, data: tf.FrameDated, frequency: int | None = None
    ) -> tf.FrameDefault:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        )

    def plot_violins(self, data: tf.FrameDated, frequency: int | None = None) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(
        self, data: tf.FrameDated, frequency: int | None = None
    ) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_boxes(self, data: tf.FrameDated, frequency: int | None = None) -> None:
        Boxes(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[tf.FrameMatrix, DefinedFunc]):
    def get_formatted_data(self, data: tf.FrameDated) -> tf.FrameMatrix:
        clean_df: tf.FrameDated = data.clean_nans(total=True)
        stats_array: nq.Float2D = self._func(clean_df.get_array())
        return tf.FrameMatrix.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        )

    def plot(self, data: tf.FrameDated) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[tf.SeriesNamed, DefinedFunc]):
    def get_formatted_data(self, data: tf.FrameDated) -> tf.SeriesNamed:
        stats_array: nq.Float2D = self._func(data.get_array())
        return tf.SeriesNamed.create_from_np(
            data=stats_array, names=data.get_names()
        ).sort_data(ascending=self._ascending)

    def plot(self, data: tf.FrameDated) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
