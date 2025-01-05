from Utilitary import ArrayFloat, DataFrameFloat, SeriesFloat, GraphFunc, STATS_GRAPHS, ROLLING_GRAPHS, OVERALL_GRAPHS
from Graphs.Transformations import sort_dataframe, sort_series, convert_multiindex_to_labels, format_returns, fill_correlation_matrix, prepare_sunburst_data
import Graphs.Widgets as Widgets 
import Metrics as Computations
from ConfigClasses import generate_dynamic_clusters
from collections.abc import Callable
import plotly.graph_objects as go # type: ignore
from Indicators.Indics_Raw import smoothed_skewness
from DataBase import process_html_temp_file

def format_metric_name(name: str) -> str:
    return name.replace("calculate_", "").replace("overall_", "").replace("_", " ").title()

def format_plot_name(name: str) -> str:
    return name.replace("plot", "").replace("_", " ").title()

def generate_html_or_show(fig: go.Figure, as_html: bool) -> str|go.Figure:
    if as_html:
        html_fig = fig.to_html(full_html=True, include_plotlyjs="True", config={"responsive": True})  # type: ignore
        return process_html_temp_file(html_content=html_fig)  # type: ignore
    return fig.show() # type: ignore

class GraphsCollection:
    def __init__(self, length: int, max_clusters: int, returns_limit: float) -> None:
        self.length: int = length
        self.max_clusters: int = max_clusters
        self.returns_limit: float = returns_limit
        self.all_plots_dict: dict[str, dict[str, GraphFunc]] = self.get_all_plots_dict()
        self.global_returns: DataFrameFloat
        self.sub_portfolio_roll: DataFrameFloat
        self.sub_portfolio_ovrll: DataFrameFloat

    def get_all_plots_dict(self) -> dict[str, dict[str, GraphFunc]]:
        all_plots_dict: dict[str, dict[str, GraphFunc]] = {
            OVERALL_GRAPHS: {},
            ROLLING_GRAPHS: {},
            STATS_GRAPHS : {}
        }
        
        for method in dir(self):
            if method.startswith("plot_"):
                category_name: str = method.split("_")[1].title()
                name: str = format_plot_name(name=method)
                func: GraphFunc = getattr(self, method)
                all_plots_dict[category_name][name] = func
        return all_plots_dict

    def get_metrics(self) -> dict[str, float]:
        metric_functions: list[Callable[..., ArrayFloat]] = [
            Computations.calculate_total_returns,
            Computations.overall_sharpe_ratio,
            Computations.calculate_max_drawdown,
            Computations.overall_volatility_annualized,
            #Computations.calculate_overall_monthly_skewness,
        ]

        metric_names: list[str] = [format_metric_name(name=func.__name__)
                    for func in metric_functions]
        results: list[ArrayFloat] = [func(self.global_returns.nparray) for func in metric_functions]

        return {
            name: round(number=result.item(), ndigits=2)
            for name, result in zip(metric_names, results)
        }

    def plot_stats_equity(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        equity_curves_df = DataFrameFloat(
            data=Computations.calculate_equity_curves(returns_array=self.sub_portfolio_roll.nparray),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll)
        )

        sorted_equity_curves: DataFrameFloat = sort_dataframe(
            df=equity_curves_df,
            use_final=True,
            ascending=True
        )

        fig: go.Figure = Widgets.curves(
            returns_df=sorted_equity_curves,
            title=format_plot_name(name=self.plot_stats_equity.__name__),
            log_scale=True,
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_rolling_volatility(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        rolling_volatility_df = DataFrameFloat(
            data=Computations.hv_composite(returns_array=self.sub_portfolio_roll.nparray),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll)
        )

        sorted_rolling_volatility_df: DataFrameFloat = sort_dataframe(
            df=rolling_volatility_df,
            ascending=False
        )

        fig: go.Figure = Widgets.curves(
            returns_df=sorted_rolling_volatility_df,
            title=format_plot_name(name=self.plot_rolling_volatility.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_rolling_drawdown(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        drawdowns_df = DataFrameFloat(
            data=Computations.calculate_rolling_drawdown(returns_array=self.sub_portfolio_roll.nparray, length=self.length),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll)
        )

        sorted_drawdowns_df: DataFrameFloat = sort_dataframe(
            df=drawdowns_df,
            ascending=True
        )

        fig: go.Figure = Widgets.curves(
            returns_df=sorted_drawdowns_df,
            title=format_plot_name(name=self.plot_rolling_drawdown.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_rolling_sharpe_ratio(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        rolling_sharpe_ratio_df = DataFrameFloat(
            data=Computations.rolling_sharpe_ratios(
                returns_array=self.sub_portfolio_roll.nparray, 
                length=self.length, 
                min_length=self.length
                ),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll)
        )

        sorted_rolling_sharpe_ratio_df: DataFrameFloat = sort_dataframe(
            df=rolling_sharpe_ratio_df,
            ascending=True
        )

        fig: go.Figure = Widgets.curves(
            returns_df=sorted_rolling_sharpe_ratio_df,
            title=format_plot_name(name=self.plot_rolling_sharpe_ratio.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_rolling_smoothed_skewness(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        rolling_skewness_df = DataFrameFloat(
            data=smoothed_skewness(returns_array=self.sub_portfolio_roll.nparray, LenSmooth=20, LenSkew=self.length),
            index=self.sub_portfolio_roll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_roll)
        )

        sorted_rolling_skewness_df: DataFrameFloat = sort_dataframe(
            df=rolling_skewness_df,
            ascending=True
        )

        fig: go.Figure = Widgets.curves(
            returns_df=sorted_rolling_skewness_df,
            title=format_plot_name(name=self.plot_rolling_smoothed_skewness.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_returns(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        total_returns_series = SeriesFloat(
            data=Computations.calculate_total_returns(returns_array=self.sub_portfolio_ovrll.nparray),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_total_returns: SeriesFloat = sort_series(series=total_returns_series, ascending=True)

        fig: go.Figure = Widgets.bars(
            series=sorted_total_returns,
            title=format_plot_name(name=self.plot_overall_returns.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_sharpe_ratio(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        sharpes_series = SeriesFloat(
            data=Computations.overall_sharpe_ratio(returns_array=self.sub_portfolio_ovrll.nparray),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_sharpes_series: SeriesFloat = sort_series(series=sharpes_series, ascending=True)

        fig: go.Figure = Widgets.bars(
            series=sorted_sharpes_series,
            title=format_plot_name(name=self.plot_overall_sharpe_ratio.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_volatility(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        overall_vol_series = SeriesFloat(
            data=Computations.overall_volatility_annualized(returns_array=self.sub_portfolio_ovrll.nparray),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_volatility: SeriesFloat = sort_series(series=overall_vol_series, ascending=True)

        fig: go.Figure = Widgets.bars(
            series=sorted_volatility,
            title=format_plot_name(name=self.plot_overall_volatility.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_average_drawdown(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        rolling_dd: ArrayFloat = Computations.calculate_rolling_drawdown(returns_array=self.sub_portfolio_ovrll.nparray, length=self.sub_portfolio_ovrll.shape[0])
        
        drawdowns_series = SeriesFloat(
            data=Computations.calculate_overall_mean(array=rolling_dd),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_drawdowns: SeriesFloat = sort_series(series=drawdowns_series, ascending=True)

        fig: go.Figure = Widgets.bars(
            series=sorted_drawdowns,
            title=format_plot_name(name=self.plot_overall_average_drawdown.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_average_correlation(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        overall_average_corr = SeriesFloat(
            data=Computations.calculate_overall_average_correlation(returns_array=self.sub_portfolio_ovrll.nparray),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_overall_average_corr: SeriesFloat = sort_series(series=overall_average_corr, ascending=True)
        fig: go.Figure = Widgets.bars(
            series=sorted_overall_average_corr,
            title=format_plot_name(name=self.plot_overall_average_correlation.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_overall_monthly_skew(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        skew_series: SeriesFloat = SeriesFloat(
            data=Computations.calculate_overall_monthly_skewness(returns_array=self.sub_portfolio_ovrll.nparray),
            index=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        sorted_skew_series: SeriesFloat = sort_series(series=skew_series, ascending=True)

        fig: go.Figure = Widgets.bars(
            series=sorted_skew_series,
            title=format_plot_name(name=self.plot_overall_monthly_skew.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_stats_distribution_violin(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        formatted_pct_returns_df = DataFrameFloat(
            data=format_returns(returns_array=self.sub_portfolio_ovrll.nparray, limit=self.returns_limit),
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )

        fig: go.Figure = Widgets.violin(
            data=formatted_pct_returns_df,
            title=format_plot_name(name=self.plot_stats_distribution_violin.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_stats_distribution_histogram(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        formatted_pct_returns_df = DataFrameFloat(
            data=format_returns(returns_array=self.sub_portfolio_ovrll.nparray, limit=self.returns_limit),
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )

        fig: go.Figure = Widgets.histogram(
            data=formatted_pct_returns_df,
            title=format_plot_name(name=self.plot_stats_distribution_histogram.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_stats_correlation_heatmap(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        correlation_matrix: ArrayFloat = Computations.calculate_correlation_matrix(returns_array=self.sub_portfolio_ovrll.nparray)
        filled_correlation_matrix: ArrayFloat = fill_correlation_matrix(corr_matrix=correlation_matrix)
        labels_list: list[str] = convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        fig: go.Figure = Widgets.heatmap(
            z_values=filled_correlation_matrix,
            x_labels=labels_list,
            y_labels=labels_list,
            title=format_plot_name(name=self.plot_stats_correlation_heatmap.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)

    def plot_stats_clusters_icicle(self, show_legend: bool = True, as_html: bool = False) -> str|go.Figure:
        renamed_returns_df = DataFrameFloat(
            data=self.sub_portfolio_ovrll.nparray,
            index=self.sub_portfolio_ovrll.dates,
            columns=convert_multiindex_to_labels(df=self.sub_portfolio_ovrll)
        )
        clusters_dict: dict[str, list[str]] = generate_dynamic_clusters(
            returns_df=renamed_returns_df,
            max_clusters=self.max_clusters
        )
        labels, parents = prepare_sunburst_data(cluster_dict=clusters_dict)

        fig: go.Figure = Widgets.icicle(
            labels=labels,
            parents=parents,
            title=format_plot_name(name=self.plot_stats_clusters_icicle.__name__),
            show_legend=show_legend
        )

        return generate_html_or_show(fig=fig, as_html=as_html)
