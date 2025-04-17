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
    D: tf.FrameDefault | dict[str, float],
    F: Callable[..., nq.Float2D],
](ABC):
    _func: F
    _ascending: bool = field(default=True)

    @property
    def _name(self) -> str:
        return self._func.__name__.replace("get", "").replace("_", " ").title()

    @abstractmethod
    def get_formatted_data(self, data: tf.FrameDefault, *args: Any, **kwargs: Any) -> D:
        raise NotImplementedError


class EquityProcessor(StatProcessor[tf.FrameDefault, OptionalFunc]):
    def get_formatted_data(
        self, data: tf.FrameDefault, frequency: int | None = None
    ) -> tf.FrameDefault:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: tf.FrameDefault, frequency: int | None = None) -> None:
        LogCurves(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class RollingProcessor(StatProcessor[tf.FrameDefault, ParametrableFunc]):
    def get_formatted_data(self, data: tf.FrameDefault, length: int) -> tf.FrameDefault:
        stats_array: nq.Float2D = self._func(data.get_array(), length)

        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        ).sort_data(ascending=self._ascending)

    def plot(self, data: tf.FrameDefault, length: int) -> None:
        Curves(
            formatted_data=self.get_formatted_data(data=data, length=length),
            title=self._name,
        )


class SamplingProcessor(StatProcessor[tf.FrameDefault, OptionalFunc]):
    def get_formatted_data(
        self, data: tf.FrameDefault, frequency: int | None = None
    ) -> tf.FrameDefault:
        stats_array: nq.Float2D = self._func(data.get_array(), frequency)
        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        )

    def plot_violins(self, data: tf.FrameDefault, frequency: int | None = None) -> None:
        Violins(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_histograms(
        self, data: tf.FrameDefault, frequency: int | None = None
    ) -> None:
        Histograms(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )

    def plot_boxes(self, data: tf.FrameDefault, frequency: int | None = None) -> None:
        Boxes(
            formatted_data=self.get_formatted_data(data=data, frequency=frequency),
            title=self._name,
        )


class TableProcessor(StatProcessor[tf.FrameDefault, DefinedFunc]):
    def get_formatted_data(self, data: tf.FrameDefault) -> tf.FrameDefault:
        clean_df: tf.FrameDefault = data.clean_nans(total=True)
        stats_array: nq.Float2D = self._func(clean_df.get_array())
        return tf.FrameDefault.create_from_np(
            data=stats_array,
            asset_names=data.get_names(),
        )

    def plot(self, data: tf.FrameDefault) -> None:
        HeatMap(formatted_data=self.get_formatted_data(data=data), title=self._name)


class AggregateProcessor(StatProcessor[dict[str, float], DefinedFunc]):
    def get_formatted_data(self, data: tf.FrameDefault) -> dict[str, float]:
        stats_array: nq.Float2D = self._func(data.get_array())
        data_dict = dict(zip(data.get_names(), stats_array.flatten()))
        return dict(
            sorted(data_dict.items(), key=lambda item: item[1], reverse=self._ascending)
        )

    def plot(self, data: tf.FrameDefault) -> None:
        Bars(formatted_data=self.get_formatted_data(data=data), title=self._name)
