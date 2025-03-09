import outquantlab.metrics as mt
from outquantlab.stats.interfaces import (
    get_df_stats_interface,
    get_series_stats_interface,
)
from outquantlab.typing_conventions import (
    ArrayFloat,
    DataFrameFloat,
    SeriesFloat,
    OverallStatFunc,
)


def _format_metric_name(name: str) -> str:
    return (
        name.replace("calculate_", "").replace("overall_", "").replace("_", " ").title()
    )


def get_metrics(returns_df: DataFrameFloat) -> dict[str, float]:
    array: ArrayFloat = returns_df.get_array()
    if array.shape[1] > 1:
        print("Metrics can only be calculated for a single asset")
        return {}
    else:
        metric_functions: list[OverallStatFunc] = [
            mt.calculate_total_returns,
            mt.overall_sharpe_ratio,
            mt.calculate_max_drawdown,
            mt.overall_volatility_annualized,
        ]

        metric_names: list[str] = [
            _format_metric_name(name=func.__name__) for func in metric_functions
        ]
        results: list[ArrayFloat] = [func(array) for func in metric_functions]

        return {
            name: round(number=result.item(), ndigits=2)
            for name, result in zip(metric_names, results)
        }


def get_stats_equity(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_equity_curves,
        ascending=True,
        length=length,
    )


def get_rolling_volatility(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.rolling_volatility,
        ascending=False,
        length=length,
    )


def get_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_rolling_drawdown,
        ascending=False,
        length=length,
    )


def get_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.rolling_sharpe_ratio,
        ascending=False,
        length=length,
    )


def get_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.rolling_skewness,
        ascending=True,
        length=length,
    )


def get_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_total_returns,
        ascending=True,
    )


def get_overall_sharpe_ratio(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.overall_sharpe_ratio,
        ascending=False,
    )


def get_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.overall_volatility_annualized,
        ascending=True,
    )


def get_overall_average_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_overall_average_drawdown,
        ascending=True,
    )


def get_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_overall_average_correlation,
        ascending=True,
    )


def get_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:
    return get_series_stats_interface(
        returns_df=returns_df,
        stats_func=mt.calculate_overall_monthly_skewness,
        ascending=True,
    )


def get_stats_distribution_violin(
    returns_df: DataFrameFloat, returns_limit: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.limit_outliers,
        ascending=True,
        length=returns_limit,
    )


def get_stats_distribution_histogram(
    returns_df: DataFrameFloat, returns_limit: int
) -> DataFrameFloat:
    return get_df_stats_interface(
        returns_df=returns_df,
        stats_func=mt.limit_outliers,
        ascending=True,
        length=returns_limit,
    )


def get_correlation_heatmap(
    returns_df: DataFrameFloat,
) -> DataFrameFloat:
    return DataFrameFloat(
        data=mt.get_filled_correlation_matrix(returns_array=returns_df.get_array()),
        columns=returns_df.get_names(),
    )


def get_correlation_clusters_icicle(
    returns_df: DataFrameFloat, max_clusters: int
) -> dict[str, list[str]]:
    return mt.get_clusters(
        returns_array=returns_df.get_array(),
        asset_names=returns_df.get_names(),
        max_clusters=max_clusters,
    )
