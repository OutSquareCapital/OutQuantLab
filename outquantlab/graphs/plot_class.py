import outquantlab.metrics as mt
from outquantlab.graphs.graph_class import Graph
from outquantlab.graphs.stats_class import (
    StatsDF,
    StatsOverall,
    StatsSeries,
)
from outquantlab.graphs.widgets import (
    Bars,
    Curves,
    Histogram,
    Table,
    Violins,
)
from outquantlab.typing_conventions import DataFrameFloat


class Plots:
    def __init__(self) -> None:
        self.curves = Curves()
        self.violins = Violins()
        self.table = Table()
        self.bars = Bars()
        self.histogram = Histogram()

    def return_data(self, returns_df: DataFrameFloat) -> StatsSeries:
        return StatsSeries(
            data=returns_df,
            func=mt.get_total_returns,
            ascending=True,
        )
    
    def plot_stats_equity(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.get_equity_curves,
            ascending=True,
            length=length,
        )
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_rolling_volatility(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.get_rolling_volatility,
            ascending=False,
            length=length,
        )
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_rolling_drawdown(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.get_rolling_drawdown,
            ascending=False,
            length=length,
        )
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_rolling_sharpe_ratio(
        self, returns_df: DataFrameFloat, length: int
    ) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.rolling_sharpe_ratio,
            ascending=True,
            length=length,
        )
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_rolling_smoothed_skewness(
        self, returns_df: DataFrameFloat, length: int
    ) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.rolling_skewness,
            ascending=True,
            length=length,
        )
        return self.curves.get_fig(data=processor.data, title=processor.title)

    def plot_stats_distribution_violin(
        self, returns_df: DataFrameFloat, returns_limit: int
    ) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.get_returns_distribution,
            ascending=True,
            length=returns_limit,
        )
        return self.violins.get_fig(data=processor.data, title=processor.title)

    def plot_stats_distribution_histogram(
        self, returns_df: DataFrameFloat, returns_limit: int
    ) -> Graph:
        processor = StatsDF(
            data=returns_df,
            func=mt.get_returns_distribution,
            ascending=True,
            length=returns_limit,
        )
        return self.histogram.get_fig(data=processor.data, title=processor.title)

    def plot_overall_returns(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.get_total_returns,
            ascending=True,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_sharpe_ratio(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.overall_sharpe_ratio,
            ascending=True,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_volatility(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.overall_volatility_annualized,
            ascending=False,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_average_drawdown(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.get_overall_average_drawdown,
            ascending=False,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_average_correlation(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.get_overall_average_correlation,
            ascending=False,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_monthly_skew(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            data=returns_df,
            func=mt.get_overall_monthly_skewness,
            ascending=True,
        )
        return self.bars.get_fig(data=processor.data, title=processor.title)

    def plot_overall_stats(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsOverall(data=returns_df)
        return self.table.get_fig(data=processor.data, title=processor.title)
