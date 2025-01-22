from typing_conventions import ArrayFloat, DataFrameFloat, SeriesFloat
from stats.transformations import (
    sort_dataframe,
    sort_series,
    convert_multiindex_to_labels,
    format_returns,
    fill_correlation_matrix,
    prepare_sunburst_data,
    normalize_data_for_colormap
)
import metrics as Computations
from config_classes import generate_dynamic_clusters
from collections.abc import Callable
from indicators.indics_raw import smoothed_skewness


def format_metric_name(name: str) -> str:
    return (
        name.replace("calculate_", "").replace("overall_", "").replace("_", " ").title()
    )


class BacktestStats:
    def __init__(
        self,
        length: int,
        max_clusters: int,
        returns_limit: float,
        initial_data: DataFrameFloat,
    ) -> None:
        self.length: int = length
        self.max_clusters: int = max_clusters
        self.returns_limit: float = returns_limit
        self.global_returns: DataFrameFloat = initial_data
        self.sub_portfolio_roll: DataFrameFloat = initial_data
        self.sub_portfolio_ovrll: DataFrameFloat = initial_data

    def get_metrics(self) -> dict[str, float]:
        metric_functions: list[Callable[..., ArrayFloat]] = [
            Computations.calculate_total_returns,
            Computations.overall_sharpe_ratio,
            Computations.calculate_max_drawdown,
            Computations.overall_volatility_annualized,
            # Computations.calculate_overall_monthly_skewness,
        ]

        metric_names: list[str] = [
            format_metric_name(name=func.__name__) for func in metric_functions
        ]
        results: list[ArrayFloat] = [
            func(self.global_returns.nparray) for func in metric_functions
        ]

        return {
            name: round(number=result.item(), ndigits=2)
            for name, result in zip(metric_names, results)
        }

    def get_stats_equity(self) -> DataFrameFloat:
        equity_curves_df = DataFrameFloat(
            data=Computations.calculate_equity_curves(
                returns_array=self.sub_portfolio_roll.nparray
            ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll),
        )

        return sort_dataframe(df=equity_curves_df, use_final=True, ascending=True)

    def get_rolling_volatility(self) -> DataFrameFloat:
        rolling_volatility_df = DataFrameFloat(
            data=Computations.hv_composite(
                returns_array=self.sub_portfolio_roll.nparray
            ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_volatility_df, ascending=False)

    def get_rolling_drawdown(self) -> DataFrameFloat:
        drawdowns_df = DataFrameFloat(
            data=Computations.calculate_rolling_drawdown(
                returns_array=self.sub_portfolio_roll.nparray, length=self.length
            ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll),
        )

        return sort_dataframe(df=drawdowns_df, ascending=True)

    def get_rolling_sharpe_ratio(self) -> DataFrameFloat:
        rolling_sharpe_ratio_df = DataFrameFloat(
            data=Computations.rolling_sharpe_ratios(
                returns_array=self.sub_portfolio_roll.nparray,
                length=self.length,
                min_length=self.length,
            ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_sharpe_ratio_df, ascending=True)

    def get_rolling_smoothed_skewness(self) -> DataFrameFloat:
        rolling_skewness_df = DataFrameFloat(
            data=smoothed_skewness(
                log_returns_array=self.sub_portfolio_roll.nparray,
                LenSmooth=20,
                LenSkew=self.length,
            ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_skewness_df, ascending=True)

    def get_overall_returns(self) -> SeriesFloat:
        total_returns_series = SeriesFloat(
            data=Computations.calculate_total_returns(
                returns_array=self.sub_portfolio_ovrll.nparray
            ),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=total_returns_series, ascending=True)

    def get_overall_sharpe_ratio(self) -> SeriesFloat:
        sharpes_series = SeriesFloat(
            data=Computations.overall_sharpe_ratio(
                returns_array=self.sub_portfolio_ovrll.nparray
            ),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=sharpes_series, ascending=True)

    def get_overall_volatility(self) -> SeriesFloat:
        overall_vol_series = SeriesFloat(
            data=Computations.overall_volatility_annualized(
                returns_array=self.sub_portfolio_ovrll.nparray
            ),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=overall_vol_series, ascending=True)

    def get_overall_average_drawdown(self) -> SeriesFloat:
        rolling_dd: ArrayFloat = Computations.calculate_rolling_drawdown(
            returns_array=self.sub_portfolio_ovrll.nparray,
            length=self.sub_portfolio_ovrll.shape[0],
        )

        drawdowns_series = SeriesFloat(
            data=Computations.calculate_overall_mean(array=rolling_dd),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=drawdowns_series, ascending=True)

    def get_overall_average_correlation(self) -> SeriesFloat:
        overall_average_corr = SeriesFloat(
            data=Computations.calculate_overall_average_correlation(
                returns_array=self.sub_portfolio_ovrll.nparray
            ),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=overall_average_corr, ascending=True)

    def get_overall_monthly_skew(self) -> SeriesFloat:
        skew_series: SeriesFloat = SeriesFloat(
            data=Computations.calculate_overall_monthly_skewness(
                returns_array=self.sub_portfolio_ovrll.nparray
            ),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

        return sort_series(series=skew_series, ascending=True)

    def get_stats_distribution_violin(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=format_returns(
                returns_array=self.sub_portfolio_ovrll.nparray, limit=self.returns_limit
            ),
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

    def get_stats_distribution_histogram(self) -> DataFrameFloat:
        return DataFrameFloat(
            data=format_returns(
                returns_array=self.sub_portfolio_ovrll.nparray, limit=self.returns_limit
            ),
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )

    def get_correlation_heatmap(self) -> tuple[ArrayFloat, list[str], ArrayFloat]:
        correlation_matrix: ArrayFloat = Computations.calculate_correlation_matrix(
            returns_array=self.sub_portfolio_ovrll.nparray
        )
        filled_correlation_matrix: ArrayFloat = fill_correlation_matrix(
            corr_matrix=correlation_matrix
        )
        labels_list: list[str] = convert_multiindex_to_labels(
            df=self.sub_portfolio_ovrll
        )
        corr_matrix_normalised = normalize_data_for_colormap(data=filled_correlation_matrix)

        return filled_correlation_matrix, labels_list, corr_matrix_normalised

    def get_correlation_clusters_icicle(self) -> tuple[list[str], list[str]]:
        renamed_returns_df = DataFrameFloat(
            data=self.sub_portfolio_ovrll.nparray,
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll),
        )
        clusters_dict: dict[str, list[str]] = generate_dynamic_clusters(
            returns_df=renamed_returns_df, max_clusters=self.max_clusters
        )
        labels, parents = prepare_sunburst_data(cluster_dict=clusters_dict)

        return labels, parents
