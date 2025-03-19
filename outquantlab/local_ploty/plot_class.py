from outquantlab.local_ploty.widgets import (
    Bars,
    Curves,
    Histogram,
    Table,
    Violins,
    HeatMap
)
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from collections.abc import Callable
from typing import TypeAlias, Protocol

class DFProcessor(Protocol):
    data: DataFrameFloat
    title: str

class SeriesProcessor(Protocol):
    data: SeriesFloat
    title: str

ParametrableDF: TypeAlias = Callable[[DataFrameFloat, int], DFProcessor]
AggregateSeries: TypeAlias = Callable[[DataFrameFloat], SeriesProcessor]
AggregateDF: TypeAlias = Callable[[DataFrameFloat], DFProcessor]


class Plots:
    def __init__(self) -> None:
        self.curves = Curves()
        self.violins = Violins()
        self.table = Table()
        self.bars = Bars()
        self.histogram = Histogram()
        self.heatmap = HeatMap()

    def plot_curves(
        self, returns_df: DataFrameFloat, length: int, stats_method: ParametrableDF
    ) -> None:
        processor: DFProcessor = stats_method(returns_df, length)
        return self.curves.get_fig(data=processor.data, title=processor.title).show()

    def plot_bars(
        self, returns_df: DataFrameFloat, stats_method: AggregateSeries
    ) -> None:
        processor: SeriesProcessor = stats_method(returns_df)
        return self.bars.get_fig(data=processor.data, title=processor.title).show()

    def plot_table(
        self, returns_df: DataFrameFloat, stats_method: AggregateSeries
    ) -> None:
        processor: SeriesProcessor = stats_method(returns_df)
        return self.table.get_fig(data=processor.data, title=processor.title).show()

    def plot_violins(
        self,
        returns_df: DataFrameFloat,
        stats_method: ParametrableDF,
        frequency: int,
    ) -> None:
        processor: DFProcessor = stats_method(returns_df, frequency)
        return self.violins.get_fig(data=processor.data, title=processor.title).show()

    def plot_histogram(
        self,
        returns_df: DataFrameFloat,
        stats_method: ParametrableDF,
        frequency: int,
    ) -> None:
        processor: DFProcessor = stats_method(returns_df, frequency)
        return self.histogram.get_fig(data=processor.data, title=processor.title).show()

    def plot_heatmap(self, returns_df: DataFrameFloat, stats_method: AggregateDF) -> None:
        processor: DFProcessor = stats_method(returns_df)
        return self.heatmap.get_fig(data=processor.data, title=processor.title).show()