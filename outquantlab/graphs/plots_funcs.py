import plotly.graph_objects as go  # type: ignore

import outquantlab.graphs.widgets_funcs as widgets_funcs
import outquantlab.stats as stats
from outquantlab.graphs.plots_interfaces import (
    get_df_plot_interface,
    get_serie_plot_interface,
)
from outquantlab.graphs.widget_class import Graph
from outquantlab.graphs.widget_implementations import Curves, Violins
from outquantlab.typing_conventions import DataFrameFloat
from outquantlab.graphs.stats_class import DataProcessorDF

def plot_metrics(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.table,
        stats_func=stats.get_metrics,
    )


def plot_stats_equity(returns_df: DataFrameFloat, length: int) -> Graph:
    processor: DataProcessorDF = DataProcessorDF(func=stats.get_stats_equity)
    data: DataFrameFloat = processor.process(data=returns_df, length=length)
    return Curves().get_fig(data=data, title=processor.title)


def plot_rolling_volatility(returns_df: DataFrameFloat, length: int) -> go.Figure:
    return get_df_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.curves,
        stats_func=stats.get_rolling_volatility,
        length=length,
    )


def plot_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> go.Figure:
    return get_df_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.curves,
        stats_func=stats.get_rolling_drawdown,
        length=length,
    )


def plot_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> go.Figure:
    return get_df_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.curves,
        stats_func=stats.get_rolling_sharpe_ratio,
        length=length,
    )


def plot_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int
) -> go.Figure:
    return get_df_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.curves,
        stats_func=stats.get_rolling_smoothed_skewness,
        length=length,
    )


def plot_overall_returns(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_returns,
    )


def plot_overall_sharpe_ratio(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_sharpe_ratio,
    )


def plot_overall_volatility(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_volatility,
    )


def plot_overall_average_drawdown(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_average_drawdown,
    )


def plot_overall_average_correlation(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_average_correlation,
    )


def plot_overall_monthly_skew(returns_df: DataFrameFloat) -> go.Figure:
    return get_serie_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.bars,
        stats_func=stats.get_overall_monthly_skew,
    )


def plot_stats_distribution_violin(
    returns_df: DataFrameFloat, returns_limit: int
) -> Graph:
    processor = DataProcessorDF(
        func=stats.get_stats_distribution_violin
    )
    data: DataFrameFloat = processor.process(data=returns_df, length=returns_limit)
    return Violins().get_fig(data=data, title=processor.title)


def plot_stats_distribution_histogram(
    returns_df: DataFrameFloat, returns_limit: int
) -> go.Figure:
    return get_df_plot_interface(
        returns_df=returns_df,
        widget_func=widgets_funcs.histogram,
        stats_func=stats.get_stats_distribution_histogram,
        length=returns_limit,
    )
