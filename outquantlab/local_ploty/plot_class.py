from outquantlab.stats import (
    StatsCurves,
    StatsOverall,
    StatsBars,
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

CurvesMethod: TypeAlias = Callable[[DataFrameFloat, int], StatsCurves]
BarsMethod: TypeAlias = Callable[[DataFrameFloat], StatsBars]
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
        self, returns_df: DataFrameFloat, length: int, stats_method: CurvesMethod
    ) -> None:
        processor: StatsCurves = stats_method(returns_df, length)
        return self.curves.get_fig(data=processor.data, title=processor.title).show()

    def plot_bars(
        self, returns_df: DataFrameFloat, stats_method: BarsMethod
    ) -> None:
        processor: StatsBars = stats_method(returns_df)
        return self.bars.get_fig(data=processor.data, title=processor.title).show()

    def plot_table(
        self, returns_df: DataFrameFloat, stats_method: OverallMethod
    ) -> None:
        processor: StatsOverall = stats_method(returns_df)
        return self.table.get_fig(data=processor.data, title=processor.title).show()

    def plot_violins(
        self,
        returns_df: DataFrameFloat,
        stats_method: DistributionMethod,
        frequency: int,
    ) -> None:
        processor: StatsDistribution = stats_method(returns_df, frequency)
        return self.violins.get_fig(data=processor.data, title=processor.title).show()

    def plot_histogram(
        self,
        returns_df: DataFrameFloat,
        stats_method: DistributionMethod,
        frequency: int,
    ) -> None:
        processor: StatsDistribution = stats_method(returns_df, frequency)
        return self.histogram.get_fig(data=processor.data, title=processor.title).show()
