import outquantlab.metrics as mt
from outquantlab.stats.stats_interfaces import (
    get_df_stats_interface,
    get_series_stats_interface,
)
from outquantlab.typing_conventions import DataFrameFloat, SeriesFloat


def get_stats_equity(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_equity_curves,
        ascending=True,
        length=length,
    )


def get_rolling_volatility(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.rolling_volatility,
        ascending=False,
        length=length,
    )


def get_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_rolling_drawdown,
        ascending=False,
        length=length,
    )


def get_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.rolling_sharpe_ratio,
        ascending=False,
        length=length,
    )


def get_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.rolling_skewness,
        ascending=True,
        length=length,
    )


def get_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_total_returns,
        ascending=True,
    )


def get_overall_sharpe_ratio(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.overall_sharpe_ratio,
        ascending=False,
    )


def get_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.overall_volatility_annualized,
        ascending=True,
    )


def get_overall_average_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_overall_average_drawdown,
        ascending=True,
    )


def get_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_overall_average_correlation,
        ascending=True,
    )


def get_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        metric_func=mt.calculate_overall_monthly_skewness,
        ascending=True,
    )


def get_stats_distribution_violin(
    returns_df: DataFrameFloat, returns_limit: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.limit_outliers,
        ascending=True,
        length=returns_limit,
    )


def get_stats_distribution_histogram(
    returns_df: DataFrameFloat, returns_limit: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        metric_func=mt.limit_outliers,
        ascending=True,
        length=returns_limit,
    )
