from outquantlab.local_ploty.graph_class import Graph
from outquantlab.stats import (
    StatsDF,
    StatsOverall,
    StatsSeries,
    StatsDistribution,
)
from outquantlab.local_ploty.widgets import (
    Bars,
    Curves,
    Histogram,
    Table,
    Violins,
)
from outquantlab.typing_conventions import DataFrameFloat
from collections.abc import Callable
from typing import TypeAlias

DFMethod: TypeAlias = Callable[[DataFrameFloat, int], StatsDF]
SeriesMethod: TypeAlias = Callable[[DataFrameFloat], StatsSeries]
OverallMethod: TypeAlias = Callable[[DataFrameFloat], StatsOverall]
DistributionMethod: TypeAlias = Callable[[DataFrameFloat, int], StatsDistribution]


class Plots:
    def __init__(self) -> None:
        self.curves = Curves()
        self.violins = Violins()
        self.table = Table()
        self.bars = Bars()
        self.histogram = Histogram()

    def plot_curves(
        self, returns_df: DataFrameFloat, length: int, stats_method: DFMethod
    ) -> Graph:
        processor: StatsDF = stats_method(returns_df, length)
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_bars(
        self, returns_df: DataFrameFloat, stats_method: SeriesMethod
    ) -> Graph:
        processor: StatsSeries = stats_method(returns_df)
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_table(
        self, returns_df: DataFrameFloat, stats_method: OverallMethod
    ) -> Graph:
        processor: StatsOverall = stats_method(returns_df)
        return self.table.get_fig(data=processor.data, title=processor.title)

    def plot_violins(
        self,
        returns_df: DataFrameFloat,
        returns_limit: int,
        stats_method: DistributionMethod,
    ) -> Graph:
        processor: StatsDistribution = stats_method(returns_df, returns_limit)
        return self.violins.get_fig(data=processor.data, title=processor.title)

    def plot_histogram(
        self,
        returns_df: DataFrameFloat,
        returns_limit: int,
        stats_method: DistributionMethod,
    ) -> Graph:
        processor: StatsDistribution = stats_method(returns_df, returns_limit)
        return self.histogram.get_fig(data=processor.data, title=processor.title)
