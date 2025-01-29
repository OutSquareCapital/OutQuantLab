import plotly.graph_objects as go  # type: ignore

import outquantlab.graphs.widgets as widgets
import outquantlab.stats as stats
from outquantlab.typing_conventions import DataFrameFloat


def format_plot_name(name: str) -> str:
    return name.replace("plot", "").replace("_", " ").title()


def plot_stats_equity(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_stats_equity(returns_df=returns_df),
        title=format_plot_name(name=plot_stats_equity.__name__),
        log_scale=True,
        show_legend=show_legend,
    )


def plot_rolling_volatility(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_volatility(returns_df=returns_df),
        title=format_plot_name(name=plot_rolling_volatility.__name__),
        show_legend=show_legend,
    )


def plot_rolling_drawdown(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_drawdown(returns_df=returns_df, length=length),
        title=format_plot_name(name=plot_rolling_drawdown.__name__),
        show_legend=show_legend,
    )


def plot_rolling_sharpe_ratio(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_sharpe_ratio(returns_df=returns_df, length=length),
        title=format_plot_name(name=plot_rolling_sharpe_ratio.__name__),
        show_legend=show_legend,
    )


def plot_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_smoothed_skewness(
            returns_df=returns_df, length=length
        ),
        title=format_plot_name(name=plot_rolling_smoothed_skewness.__name__),
        show_legend=show_legend,
    )


def plot_overall_returns(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_returns(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_returns.__name__),
        show_legend=show_legend,
    )


def plot_overall_sharpe_ratio(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_sharpe_ratio(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_sharpe_ratio.__name__),
        show_legend=show_legend,
    )


def plot_overall_volatility(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_volatility(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_volatility.__name__),
        show_legend=show_legend,
    )


def plot_overall_average_drawdown(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_average_drawdown(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_average_drawdown.__name__),
        show_legend=show_legend,
    )


def plot_overall_average_correlation(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_average_correlation(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_average_correlation.__name__),
        show_legend=show_legend,
    )


def plot_overall_monthly_skew(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_monthly_skew(returns_df=returns_df),
        title=format_plot_name(name=plot_overall_monthly_skew.__name__),
        show_legend=show_legend,
    )


def plot_stats_distribution_violin(
    returns_df: DataFrameFloat, returns_limit: int, show_legend: bool = True
) -> go.Figure:
    return widgets.violin(
        data=stats.get_stats_distribution_violin(
            returns_df=returns_df,
            returns_limit=returns_limit,
        ),
        title=format_plot_name(name=plot_stats_distribution_violin.__name__),
        show_legend=show_legend,
    )


def plot_stats_distribution_histogram(
    returns_df: DataFrameFloat, returns_limit: float, show_legend: bool = True
) -> go.Figure:
    return widgets.histogram(
        data=stats.get_stats_distribution_histogram(
            returns_df=returns_df,
            returns_limit=returns_limit,
        ),
        title=format_plot_name(name=plot_stats_distribution_histogram.__name__),
        show_legend=show_legend,
    )


def plot_correlation_heatmap(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    filled_correlation_matrix, labels_list, corr_matrix_normalised = (
        stats.get_correlation_heatmap(returns_df=returns_df)
    )

    return widgets.heatmap(
        z_values=filled_correlation_matrix,
        x_labels=labels_list,
        y_labels=labels_list,
        z_normalized=corr_matrix_normalised,
        title=format_plot_name(name=plot_correlation_heatmap.__name__),
        show_legend=show_legend,
    )


def plot_correlation_clusters_icicle(
    returns_df: DataFrameFloat, max_clusters: int, show_legend: bool = True
) -> go.Figure:
    labels, parents = stats.get_correlation_clusters_icicle(
        returns_df=returns_df, max_clusters=max_clusters
    )

    return widgets.icicle(
        labels=labels,
        parents=parents,
        title=format_plot_name(name=plot_correlation_clusters_icicle.__name__),
        show_legend=show_legend,
    )
