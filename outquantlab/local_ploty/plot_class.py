from outquantlab.local_ploty.widgets import (
    Bars,
    Curves,
    Histogram,
    Table,
    Violins,
    HeatMap,
)
from outquantlab.stats import (
    CurvesMetric,
    HistogramMetric,
    HeatMapMetric,
    BarsMetric,
    OverallMetrics,
)
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat


class Plots:
    def plot_curves(
        self, returns_df: DataFrameFloat, length: int, metric: CurvesMetric
    ) -> None:
        formatted_data: DataFrameFloat = metric.get_data(
            returns_df=returns_df, length=length
        )
        Curves(formatted_data=formatted_data, title=metric.title)

    def plot_histogram(
        self, returns_df: DataFrameFloat, frequency: int, metric: HistogramMetric
    ) -> None:
        formatted_data: DataFrameFloat = metric.get_data(
            returns_df=returns_df, frequency=frequency
        )
        Histogram(formatted_data=formatted_data, title=metric.title)

    def plot_violins(
        self, returns_df: DataFrameFloat, frequency: int, metric: HistogramMetric
    ) -> None:
        formatted_data: DataFrameFloat = metric.get_data(
            returns_df=returns_df, frequency=frequency
        )
        Violins(formatted_data=formatted_data, title=metric.title)

    def plot_bars(self, returns_df: DataFrameFloat, metric: BarsMetric) -> None:
        formatted_data: SeriesFloat = metric.get_data(returns_df=returns_df)
        Bars(formatted_data=formatted_data, title=metric.title)

    def plot_heatmap(self, returns_df: DataFrameFloat, metric: HeatMapMetric) -> None:
        formatted_data: DataFrameFloat = metric.get_data(returns_df=returns_df)
        HeatMap(formatted_data=formatted_data, title=metric.title)

    def plot_overall_metrics(
        self, returns_df: DataFrameFloat, metric: OverallMetrics
    ) -> None:
        formatted_data: SeriesFloat = metric.get_data(returns_df=returns_df)
        Table(formatted_data=formatted_data, title=metric.title)
