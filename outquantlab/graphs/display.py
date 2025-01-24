import plotly.graph_objects as go  # type: ignore

import outquantlab.graphs.widgets as widgets
from outquantlab.stats import BacktestStats


def format_plot_name(name: str) -> str:
    return name.replace("plot", "").replace("_", " ").title()


class GraphsCollection:
    def __init__(self, stats: BacktestStats) -> None:
        self.stats: BacktestStats = stats

    def plot_stats_equity(self, show_legend: bool = True) -> go.Figure:
        return widgets.curves(
            returns_df=self.stats.get_stats_equity(),
            title=format_plot_name(name=self.plot_stats_equity.__name__),
            log_scale=True,
            show_legend=show_legend,
        )

    def plot_rolling_volatility(self, show_legend: bool = True) -> go.Figure:
        return widgets.curves(
            returns_df=self.stats.get_rolling_volatility(),
            title=format_plot_name(name=self.plot_rolling_volatility.__name__),
            show_legend=show_legend,
        )

    def plot_rolling_drawdown(self, length: int, show_legend: bool = True) -> go.Figure:
        return widgets.curves(
            returns_df=self.stats.get_rolling_drawdown(length=length),
            title=format_plot_name(name=self.plot_rolling_drawdown.__name__),
            show_legend=show_legend,
        )

    def plot_rolling_sharpe_ratio(
        self, length: int, show_legend: bool = True
    ) -> go.Figure:
        return widgets.curves(
            returns_df=self.stats.get_rolling_sharpe_ratio(length=length),
            title=format_plot_name(name=self.plot_rolling_sharpe_ratio.__name__),
            show_legend=show_legend,
        )

    def plot_rolling_smoothed_skewness(
        self, length: int, show_legend: bool = True
    ) -> go.Figure:
        return widgets.curves(
            returns_df=self.stats.get_rolling_smoothed_skewness(length=length),
            title=format_plot_name(name=self.plot_rolling_smoothed_skewness.__name__),
            show_legend=show_legend,
        )

    def plot_overall_returns(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_returns(),
            title=format_plot_name(name=self.plot_overall_returns.__name__),
            show_legend=show_legend,
        )

    def plot_overall_sharpe_ratio(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_sharpe_ratio(),
            title=format_plot_name(name=self.plot_overall_sharpe_ratio.__name__),
            show_legend=show_legend,
        )

    def plot_overall_volatility(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_volatility(),
            title=format_plot_name(name=self.plot_overall_volatility.__name__),
            show_legend=show_legend,
        )

    def plot_overall_average_drawdown(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_average_drawdown(),
            title=format_plot_name(name=self.plot_overall_average_drawdown.__name__),
            show_legend=show_legend,
        )

    def plot_overall_average_correlation(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_average_correlation(),
            title=format_plot_name(name=self.plot_overall_average_correlation.__name__),
            show_legend=show_legend,
        )

    def plot_overall_monthly_skew(self, show_legend: bool = True) -> go.Figure:
        return widgets.bars(
            series=self.stats.get_overall_monthly_skew(),
            title=format_plot_name(name=self.plot_overall_monthly_skew.__name__),
            show_legend=show_legend,
        )

    def plot_stats_distribution_violin(
        self, returns_limit: int, show_legend: bool = True
    ) -> go.Figure:
        return widgets.violin(
            data=self.stats.get_stats_distribution_violin(returns_limit=returns_limit),
            title=format_plot_name(name=self.plot_stats_distribution_violin.__name__),
            show_legend=show_legend,
        )

    def plot_stats_distribution_histogram(
        self, returns_limit: float, show_legend: bool = True
    ) -> go.Figure:
        return widgets.histogram(
            data=self.stats.get_stats_distribution_histogram(
                returns_limit=returns_limit
            ),
            title=format_plot_name(
                name=self.plot_stats_distribution_histogram.__name__
            ),
            show_legend=show_legend,
        )

    def plot_correlation_heatmap(self, show_legend: bool = True) -> go.Figure:
        filled_correlation_matrix, labels_list, corr_matrix_normalised = (
            self.stats.get_correlation_heatmap()
        )

        return widgets.heatmap(
            z_values=filled_correlation_matrix,
            x_labels=labels_list,
            y_labels=labels_list,
            z_normalized=corr_matrix_normalised,
            title=format_plot_name(name=self.plot_correlation_heatmap.__name__),
            show_legend=show_legend,
        )

    def plot_correlation_clusters_icicle(
        self, max_clusters: int, show_legend: bool = True
    ) -> go.Figure:
        labels, parents = self.stats.get_correlation_clusters_icicle(
            max_clusters=max_clusters
        )

        return widgets.icicle(
            labels=labels,
            parents=parents,
            title=format_plot_name(name=self.plot_correlation_clusters_icicle.__name__),
            show_legend=show_legend,
        )
