from outquantlab.graphs.widget_implementations import (
    Curves,
    Violins,
    Table,
    Bars,
    Histogram,
)
from outquantlab.graphs.stats_class import (
    StatsDF,
    StatsSeries,
    get_metrics,
)
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat
from outquantlab.graphs.widget_class import Graph
import outquantlab.metrics as mt


class Plots:
    def __init__(self) -> None:
        self.curves = Curves()
        self.violins = Violins()
        self.table = Table()
        self.bars = Bars()
        self.histogram = Histogram()

    def plot_stats_equity(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            func=mt.get_equity_curves, ascending=True, title="Equity Curves"
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=length)
        return self.curves.get_fig(data=data, title=processor.title)

    def plot_rolling_volatility(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            func=mt.rolling_volatility, ascending=False, title="Rolling Volatility"
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=length)
        return self.curves.get_fig(data=data, title=processor.title)

    def plot_rolling_drawdown(self, returns_df: DataFrameFloat, length: int) -> Graph:
        processor = StatsDF(
            func=mt.get_rolling_drawdown,
            ascending=False,
            title="Rolling Drawdown",
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=length)
        return self.curves.get_fig(data=data, title=processor.title)

    def plot_rolling_sharpe_ratio(
        self, returns_df: DataFrameFloat, length: int
    ) -> Graph:
        processor = StatsDF(
            func=mt.rolling_sharpe_ratio, ascending=False, title="Rolling Sharpe Ratio"
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=length)
        return self.curves.get_fig(data=data, title=processor.title)

    def plot_rolling_smoothed_skewness(
        self, returns_df: DataFrameFloat, length: int
    ) -> Graph:
        processor = StatsDF(
            func=mt.rolling_skewness, ascending=True, title="Rolling Smoothed Skewness"
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=length)
        return self.curves.get_fig(data=data, title=processor.title)

    def plot_stats_distribution_violin(
        self, returns_df: DataFrameFloat, returns_limit: int
    ) -> Graph:
        processor = StatsDF(
            func=mt.limit_outliers,
            ascending=True,
            title="Distribution Violin Plot",
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=returns_limit)
        return self.violins.get_fig(data=data, title=processor.title)

    def plot_stats_distribution_histogram(
        self, returns_df: DataFrameFloat, returns_limit: int
    ) -> Graph:
        processor = StatsDF(
            func=mt.limit_outliers,
            ascending=True,
            title="Distribution Histogram Plot",
        )
        data: DataFrameFloat = processor.get_data(data=returns_df, length=returns_limit)
        return self.histogram.get_fig(data=data, title=processor.title)

    def plot_overall_returns(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.get_total_returns, ascending=True, title="Overall Returns"
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_overall_sharpe_ratio(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.overall_sharpe_ratio, ascending=False, title="Overall Sharpe Ratio"
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_overall_volatility(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.overall_volatility_annualized,
            ascending=False,
            title="Overall Volatility",
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_overall_average_drawdown(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.get_overall_average_drawdown,
            ascending=True,
            title="Overall Average Drawdown",
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_overall_average_correlation(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.get_overall_average_correlation,
            ascending=True,
            title="Overall Average Correlation",
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_overall_monthly_skew(self, returns_df: DataFrameFloat) -> Graph:
        processor = StatsSeries(
            func=mt.get_overall_monthly_skewness,
            ascending=True,
            title="Overall Monthly Skew",
        )
        data: SeriesFloat = processor.get_data(data=returns_df)
        return self.bars.get_fig(data=data, title=processor.title)

    def plot_metrics(self, returns_df: DataFrameFloat) -> Graph:
        data: SeriesFloat = get_metrics(returns_df=returns_df)
        return self.table.get_fig(data=data, title="Metrics")
