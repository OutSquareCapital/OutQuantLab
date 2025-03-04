from collections.abc import Callable

import outquantlab.metrics as mt
from outquantlab.config_classes import generate_dynamic_clusters
from outquantlab.stats.transformations import (
    convert_multiindex_to_labels,
    fill_correlation_matrix,
    format_returns,
    normalize_data_for_colormap,
    prepare_sunburst_data,
    sort_dataframe,
    sort_series,
)
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat


def _format_metric_name(name: str) -> str:
    return (
        name.replace("calculate_", "").replace("overall_", "").replace("_", " ").title()
    )


def get_metrics(returns_df: DataFrameFloat) -> dict[str, float]:
    metric_functions: list[Callable[..., ArrayFloat]] = [
        mt.calculate_total_returns,
        mt.overall_sharpe_ratio,
        mt.calculate_max_drawdown,
        mt.overall_volatility_annualized,
    ]

    metric_names: list[str] = [
        _format_metric_name(name=func.__name__) for func in metric_functions
    ]
    results: list[ArrayFloat] = [
        func(returns_df.get_array()) for func in metric_functions
    ]

    return {
        name: round(number=result.item(), ndigits=2)
        for name, result in zip(metric_names, results)
    }

def get_raw_data_formatted(returns_df: DataFrameFloat) -> DataFrameFloat:
    formatted_returns_df = DataFrameFloat(
        data=returns_df.get_array(),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )
    return sort_dataframe(df=formatted_returns_df, use_final=True, ascending=True)

def get_stats_equity(returns_df: DataFrameFloat) -> DataFrameFloat:
    equity_curves_df = DataFrameFloat(
        data=mt.calculate_equity_curves(returns_array=returns_df.get_array()),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_dataframe(df=equity_curves_df, use_final=True, ascending=True)


def get_rolling_volatility(returns_df: DataFrameFloat) -> DataFrameFloat:
    rolling_volatility_df = DataFrameFloat(
        data=mt.hv_composite(returns_array=returns_df.get_array()),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_dataframe(df=rolling_volatility_df, ascending=False)


def get_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    drawdowns_df = DataFrameFloat(
        data=mt.calculate_rolling_drawdown(
            returns_array=returns_df.get_array(),
            length=length,
        ),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_dataframe(df=drawdowns_df, ascending=True)


def get_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    rolling_sharpe_ratio_df = DataFrameFloat(
        data=mt.rolling_sharpe_ratios(
            returns_array=returns_df.get_array(),
            length=length,
            min_length=length,
        ),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_dataframe(df=rolling_sharpe_ratio_df, ascending=True)


def get_rolling_smoothed_skewness(
    returns_df: DataFrameFloat, length: int
) -> DataFrameFloat:
    rolling_skewness_df = DataFrameFloat(
        data=mt.rolling_skewness(
            array=returns_df.get_array(),
            length=length,
            min_length=length,
        ),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_dataframe(df=rolling_skewness_df, ascending=True)


def get_overall_returns(returns_df: DataFrameFloat) -> SeriesFloat:
    total_returns_series = SeriesFloat(
        data=mt.calculate_total_returns(returns_array=returns_df.get_array()),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=total_returns_series, ascending=True)


def get_overall_sharpe_ratio(returns_df: DataFrameFloat) -> SeriesFloat:
    sharpes_series = SeriesFloat(
        data=mt.overall_sharpe_ratio(returns_array=returns_df.get_array()),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=sharpes_series, ascending=True)


def get_overall_volatility(returns_df: DataFrameFloat) -> SeriesFloat:
    overall_vol_series = SeriesFloat(
        data=mt.overall_volatility_annualized(returns_array=returns_df.get_array()),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=overall_vol_series, ascending=True)


def get_overall_average_drawdown(returns_df: DataFrameFloat) -> SeriesFloat:
    rolling_dd: ArrayFloat = mt.calculate_rolling_drawdown(
        returns_array=returns_df.get_array(),
        length=returns_df.shape[0],
    )

    drawdowns_series = SeriesFloat(
        data=mt.get_overall_mean(array=rolling_dd),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=drawdowns_series, ascending=True)


def get_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:
    overall_average_corr = SeriesFloat(
        data=mt.calculate_overall_average_correlation(
            returns_array=returns_df.get_array()
        ),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=overall_average_corr, ascending=True)


def get_overall_monthly_skew(returns_df: DataFrameFloat) -> SeriesFloat:
    skew_series: SeriesFloat = SeriesFloat(
        data=mt.calculate_overall_monthly_skewness(
            returns_array=returns_df.get_array()
        ),
        index=convert_multiindex_to_labels(df=returns_df),
    )

    return sort_series(series=skew_series, ascending=True)


def get_stats_distribution_violin(
    returns_df: DataFrameFloat, returns_limit: float
) -> DataFrameFloat:
    return DataFrameFloat(
        data=format_returns(
            returns_array=returns_df.get_array(),
            limit=returns_limit,
        ),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )


def get_stats_distribution_histogram(
    returns_df: DataFrameFloat, returns_limit: float
) -> DataFrameFloat:
    return DataFrameFloat(
        data=format_returns(
            returns_array=returns_df.get_array(),
            limit=returns_limit,
        ),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )


def get_correlation_heatmap(
    returns_df: DataFrameFloat,
) -> tuple[ArrayFloat, list[str], ArrayFloat]:
    correlation_matrix: ArrayFloat = mt.calculate_correlation_matrix(
        returns_array=returns_df.get_array()
    )
    filled_correlation_matrix: ArrayFloat = fill_correlation_matrix(
        corr_matrix=correlation_matrix
    )
    labels_list: list[str] = convert_multiindex_to_labels(df=returns_df)
    corr_matrix_normalised = normalize_data_for_colormap(data=filled_correlation_matrix)

    return filled_correlation_matrix, labels_list, corr_matrix_normalised


def get_correlation_clusters_icicle(
    returns_df: DataFrameFloat, max_clusters: int
) -> tuple[list[str], list[str]]:
    renamed_returns_df = DataFrameFloat(
        data=returns_df.get_array(),
        index=returns_df.dates,
        columns=convert_multiindex_to_labels(df=returns_df),
    )
    clusters_dict: dict[str, list[str]] = generate_dynamic_clusters(
        returns_df=renamed_returns_df, max_clusters=max_clusters
    )
    labels, parents = prepare_sunburst_data(cluster_dict=clusters_dict)

    return labels, parents
