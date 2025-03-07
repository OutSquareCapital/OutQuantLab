import plotly.graph_objects as go  # type: ignore
import outquantlab.graphs.widgets as widgets
import outquantlab.stats as stats
from outquantlab.typing_conventions import DataFrameFloat


def _format_plot_name(name: str) -> str:
    return name.replace("plot", "").replace("_", " ").title()


def plot_metrics(returns_df: DataFrameFloat) -> None:
    metrics: dict[str, float] = stats.get_metrics(returns_df=returns_df)
    for key, value in metrics.items():
        print(f"{key}: {value}")


def plot_raw_data(returns_df: DataFrameFloat, show_legend: bool = True) -> go.Figure:
    return widgets.curves(
        returns_df=returns_df,
        title=_format_plot_name(name=plot_raw_data.__name__),
        show_legend=show_legend,
    )


def plot_stats_equity(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_stats_equity(returns_df=returns_df),
        title=_format_plot_name(name=plot_stats_equity.__name__),
        log_scale=True,
        show_legend=show_legend,
    )


def plot_rolling_volatility(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_volatility(returns_df=returns_df),
        title=_format_plot_name(name=plot_rolling_volatility.__name__),
        show_legend=show_legend,
    )


def plot_rolling_drawdown(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_drawdown(returns_df=returns_df, length=length),
        title=_format_plot_name(name=plot_rolling_drawdown.__name__),
        show_legend=show_legend,
    )


def plot_rolling_sharpe_ratio(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_sharpe_ratio(returns_df=returns_df, length=length),
        title=_format_plot_name(name=plot_rolling_sharpe_ratio.__name__),
        show_legend=show_legend,
    )


def plot_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int, show_legend: bool = True
) -> go.Figure:
    return widgets.curves(
        returns_df=stats.get_rolling_smoothed_skewness(
            returns_df=returns_df, length=length
        ),
        title=_format_plot_name(name=plot_rolling_smoothed_skewness.__name__),
        show_legend=show_legend,
    )


def plot_overall_returns(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_returns(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_returns.__name__),
        show_legend=show_legend,
    )


def plot_overall_sharpe_ratio(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_sharpe_ratio(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_sharpe_ratio.__name__),
        show_legend=show_legend,
    )


def plot_overall_volatility(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_volatility(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_volatility.__name__),
        show_legend=show_legend,
    )


def plot_overall_average_drawdown(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_average_drawdown(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_average_drawdown.__name__),
        show_legend=show_legend,
    )


def plot_overall_average_correlation(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_average_correlation(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_average_correlation.__name__),
        show_legend=show_legend,
    )


def plot_overall_monthly_skew(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.bars(
        series=stats.get_overall_monthly_skew(returns_df=returns_df),
        title=_format_plot_name(name=plot_overall_monthly_skew.__name__),
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
        title=_format_plot_name(name=plot_stats_distribution_violin.__name__),
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
        title=_format_plot_name(name=plot_stats_distribution_histogram.__name__),
        show_legend=show_legend,
    )


def plot_correlation_heatmap(
    returns_df: DataFrameFloat, show_legend: bool = True
) -> go.Figure:
    return widgets.heatmap(
        returns_df=stats.get_correlation_heatmap(returns_df=returns_df),
        title=_format_plot_name(name=plot_correlation_heatmap.__name__),
        show_legend=show_legend,
    )


def plot_correlation_clusters_icicle(
    returns_df: DataFrameFloat, max_clusters: int = 4, show_legend: bool = True
) -> go.Figure:
    clusters_dict: dict[str, list[str]] = stats.get_correlation_clusters_icicle(
        returns_df=returns_df, max_clusters=max_clusters
    )

    return widgets.icicle(
        clusters_dict=clusters_dict,
        title=_format_plot_name(name=plot_correlation_clusters_icicle.__name__),
        show_legend=show_legend,
    )
