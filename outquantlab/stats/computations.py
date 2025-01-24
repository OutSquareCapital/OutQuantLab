from collections.abc import Callable

import outquantlab.metrics as mt
from outquantlab.config_classes import generate_dynamic_clusters
from outquantlab.indicators import DataDfs
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


def format_metric_name(name: str) -> str:
    return (
        name.replace("calculate_", "").replace("overall_", "").replace("_", " ").title()
    )


class BacktestStats:
    def __init__(
        self,
        data_dfs: DataDfs,
    ) -> None:
        self.data_dfs: DataDfs = data_dfs

    def get_metrics(self) -> dict[str, float]:
        metric_functions: list[Callable[..., ArrayFloat]] = [
            mt.calculate_total_returns,
            mt.overall_sharpe_ratio,
            mt.calculate_max_drawdown,
            mt.overall_volatility_annualized,
            # mt.calculate_overall_monthly_skewness,
        ]

        metric_names: list[str] = [
            format_metric_name(name=func.__name__) for func in metric_functions
        ]
        results: list[ArrayFloat] = [
            func(self.data_dfs.global_returns.get_array()) for func in metric_functions
        ]

        return {
            name: round(number=result.item(), ndigits=2)
            for name, result in zip(metric_names, results)
        }

    def get_stats_equity(self) -> DataFrameFloat:
        equity_curves_df = DataFrameFloat(
            data=mt.calculate_equity_curves(
                returns_array=self.data_dfs.sub_portfolio_roll.get_array()
            ),
            index=self.data_dfs.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_roll),
        )

        return sort_dataframe(df=equity_curves_df, use_final=True, ascending=True)

    def get_rolling_volatility(self) -> DataFrameFloat:
        rolling_volatility_df = DataFrameFloat(
            data=mt.hv_composite(
                returns_array=self.data_dfs.sub_portfolio_roll.get_array()
            ),
            index=self.data_dfs.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_volatility_df, ascending=False)

    def get_rolling_drawdown(self, length: int) -> DataFrameFloat:
        drawdowns_df = DataFrameFloat(
            data=mt.calculate_rolling_drawdown(
                returns_array=self.data_dfs.sub_portfolio_roll.get_array(),
                length=length,
            ),
            index=self.data_dfs.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_roll),
        )

        return sort_dataframe(df=drawdowns_df, ascending=True)

    def get_rolling_sharpe_ratio(self, length: int) -> DataFrameFloat:
        rolling_sharpe_ratio_df = DataFrameFloat(
            data=mt.rolling_sharpe_ratios(
                returns_array=self.data_dfs.sub_portfolio_roll.get_array(),
                length=length,
                min_length=length,
            ),
            index=self.data_dfs.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_sharpe_ratio_df, ascending=True)

    def get_rolling_smoothed_skewness(self, length: int) -> DataFrameFloat:
        rolling_skewness_df = DataFrameFloat(
            data=mt.rolling_skewness(
                array=self.data_dfs.sub_portfolio_roll.get_array(),
                length=length,
                min_length=length,
            ),
            index=self.data_dfs.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_roll),
        )

        return sort_dataframe(df=rolling_skewness_df, ascending=True)

    def get_overall_returns(self) -> SeriesFloat:
        total_returns_series = SeriesFloat(
            data=mt.calculate_total_returns(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
            ),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=total_returns_series, ascending=True)

    def get_overall_sharpe_ratio(self) -> SeriesFloat:
        sharpes_series = SeriesFloat(
            data=mt.overall_sharpe_ratio(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
            ),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=sharpes_series, ascending=True)

    def get_overall_volatility(self) -> SeriesFloat:
        overall_vol_series = SeriesFloat(
            data=mt.overall_volatility_annualized(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
            ),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=overall_vol_series, ascending=True)

    def get_overall_average_drawdown(self) -> SeriesFloat:
        rolling_dd: ArrayFloat = mt.calculate_rolling_drawdown(
            returns_array=self.data_dfs.sub_portfolio_ovrll.get_array(),
            length=self.data_dfs.sub_portfolio_ovrll.shape[0],
        )

        drawdowns_series = SeriesFloat(
            data=mt.calculate_overall_mean(array=rolling_dd),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=drawdowns_series, ascending=True)

    def get_overall_average_correlation(self) -> SeriesFloat:
        overall_average_corr = SeriesFloat(
            data=mt.calculate_overall_average_correlation(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
            ),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=overall_average_corr, ascending=True)

    def get_overall_monthly_skew(self) -> SeriesFloat:
        skew_series: SeriesFloat = SeriesFloat(
            data=mt.calculate_overall_monthly_skewness(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
            ),
            index=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

        return sort_series(series=skew_series, ascending=True)

    def get_stats_distribution_violin(self, returns_limit: float) -> DataFrameFloat:
        return DataFrameFloat(
            data=format_returns(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array(),
                limit=returns_limit,
            ),
            index=self.data_dfs.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

    def get_stats_distribution_histogram(self, returns_limit: float) -> DataFrameFloat:
        return DataFrameFloat(
            data=format_returns(
                returns_array=self.data_dfs.sub_portfolio_ovrll.get_array(),
                limit=returns_limit,
            ),
            index=self.data_dfs.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )

    def get_correlation_heatmap(self) -> tuple[ArrayFloat, list[str], ArrayFloat]:
        correlation_matrix: ArrayFloat = mt.calculate_correlation_matrix(
            returns_array=self.data_dfs.sub_portfolio_ovrll.get_array()
        )
        filled_correlation_matrix: ArrayFloat = fill_correlation_matrix(
            corr_matrix=correlation_matrix
        )
        labels_list: list[str] = convert_multiindex_to_labels(
            df=self.data_dfs.sub_portfolio_ovrll
        )
        corr_matrix_normalised = normalize_data_for_colormap(
            data=filled_correlation_matrix
        )

        return filled_correlation_matrix, labels_list, corr_matrix_normalised

    def get_correlation_clusters_icicle(
        self, max_clusters: int
    ) -> tuple[list[str], list[str]]:
        renamed_returns_df = DataFrameFloat(
            data=self.data_dfs.sub_portfolio_ovrll.get_array(),
            index=self.data_dfs.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.data_dfs.sub_portfolio_ovrll),
        )
        clusters_dict: dict[str, list[str]] = generate_dynamic_clusters(
            returns_df=renamed_returns_df, max_clusters=max_clusters
        )
        labels, parents = prepare_sunburst_data(cluster_dict=clusters_dict)

        return labels, parents
