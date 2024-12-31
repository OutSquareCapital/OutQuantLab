from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth, SeriesFloat
from Dashboard.Transformations import sort_dataframe, sort_series, convert_multiindex_to_labels, format_returns, fill_correlation_matrix, prepare_sunburst_data
import Dashboard.Widgets as Widgets 
import Metrics as Computations
from ConfigClasses import generate_static_clusters
from collections.abc import Callable
import plotly.graph_objects as go # type: ignore
from dataclasses import dataclass
from Indicators.Indics_Raw import smoothed_skewness
from DataBase import process_html_temp_file

@dataclass
class DashboardPlot:
    name: str
    func: Callable[..., go.Figure]
    category: str
    length_required: bool

class DashboardsCollection:
    def __init__(self, length: int) -> None:
        self.global_portfolio: DataFrameFloat
        self.sub_portfolios: DataFrameFloat
        self.length: int = length
        self.all_dashboards: dict[str, DashboardPlot] = self.__initialize_dashboards()

    def __initialize_dashboards(self) -> dict[str, DashboardPlot]:
        all_dashboards: dict[str, DashboardPlot] = {}
        for name, func in self.__class__.__dict__.items():
            # Vérifie si c'est un staticmethod
            if isinstance(func, staticmethod):
                func = func.__func__  # Accède à la vraie fonction derrière le staticmethod
                if name.startswith("plot_"):
                    formatted_name: str = name[5:].replace("_", " ").title()
                    category = (
                        "overall" if "overall" in name else
                        "rolling" if "rolling" in name else
                        "other"
                    )
                    all_dashboards[formatted_name] = DashboardPlot(
                        name=formatted_name,
                        func=func,
                        category=category,
                        length_required="length" in func.__code__.co_varnames
                    )
        return all_dashboards

    @property
    def all_plots_names(self) -> list[str]:
        return list(self.all_dashboards.keys())

    @property
    def metrics(self) -> dict[str, float]:
        metric_functions: list[Callable[..., ArrayFloat]] = [
            Computations.calculate_total_returns,
            Computations.overall_sharpe_ratio,
            Computations.calculate_max_drawdown,
            Computations.overall_volatility_annualized,
            Computations.calculate_overall_monthly_skewness,
        ]

        metric_names: list[str] = [func.__name__.replace('calculate_', '').replace('overall_', '') 
                    for func in metric_functions]

        results: list[ArrayFloat] = [func(self.global_portfolio.nparray) for func in metric_functions]
        
        return {
            name: round(number=result.item(), ndigits=2)
            for name, result in zip(metric_names, results)
        }

    def get_fig(self, dashboard_name: str, global_plot:bool = False) -> go.Figure:
        
        dashboard: DashboardPlot = self.all_dashboards[dashboard_name]
        portfolio: DataFrameFloat = self.global_portfolio if global_plot else self.sub_portfolios

        if dashboard.length_required:
            return dashboard.func(portfolio, length=self.length)
        return dashboard.func(portfolio)

    def plot(self, dashboard_name: str, global_plot:bool = False, show_legend:bool=True, to_html: bool = False) -> str:
        graph_fig:go.Figure = self.get_fig(dashboard_name=dashboard_name, global_plot=global_plot) # type: ignore

        if not show_legend:
            graph_fig.update_layout(showlegend=False) # type: ignore
            
        if to_html:
            html_fig: Unknown = graph_fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True}) # type: ignore
            return process_html_temp_file(html_content=html_fig) # type: ignore

        return graph_fig.show() # type: ignore


    @staticmethod
    def plot_equity(returns_df: DataFrameFloat) -> go.Figure:
        equity_curves_df = DataFrameFloat(
            data=Computations.calculate_equity_curves(returns_array=returns_df.nparray),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
            )

        sorted_equity_curves: DataFrameFloat = sort_dataframe(
            df=equity_curves_df,
            use_final=True,
            ascending=True)

        return Widgets.curves(
            x_values=sorted_equity_curves.dates,
            y_values=sorted_equity_curves,
            title="Equity Curve", 
            log_scale=True)
    @staticmethod
    def plot_rolling_volatility(returns_df: DataFrameFloat) -> go.Figure:
        rolling_volatility_df = DataFrameFloat(
            data=Computations.hv_composite(returns_array=returns_df.nparray),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
        )

        sorted_rolling_volatility_df: DataFrameFloat = sort_dataframe(
            df=rolling_volatility_df,
            ascending=False
        )

        return Widgets.curves(
            x_values=sorted_rolling_volatility_df.dates,
            y_values=sorted_rolling_volatility_df,
            title="Rolling Volatility %"
        )
    @staticmethod
    def plot_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> go.Figure:
        drawdowns_df = DataFrameFloat(
            data=Computations.calculate_rolling_drawdown(returns_array=returns_df.nparray, length=length),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
        )

        sorted_drawdowns: DataFrameFloat = sort_dataframe(
            df=drawdowns_df,
            ascending=True
        )

        return Widgets.curves(
            x_values=sorted_drawdowns.dates,
            y_values=sorted_drawdowns,
            title="Rolling Drawdown %"
        )
    @staticmethod
    def plot_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> go.Figure:
        rolling_sharpe_ratio_df = DataFrameFloat(
            data=Computations.rolling_sharpe_ratios(returns_array=returns_df.nparray, length=length, min_length=length),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
        )

        sorted_rolling_sharpe_ratio_df: DataFrameFloat = sort_dataframe(
            df=rolling_sharpe_ratio_df,
            ascending=True
        )

        return Widgets.curves(
            x_values=sorted_rolling_sharpe_ratio_df.dates,
            y_values=sorted_rolling_sharpe_ratio_df,
            title="Rolling Sharpe Ratio"
        )
    @staticmethod
    def plot_rolling_smoothed_skewness(returns_df: DataFrameFloat, length: int) -> go.Figure:
        rolling_skewness_df = DataFrameFloat(
            data=smoothed_skewness(returns_array=returns_df.nparray, LenSmooth=length, LenSkew=length),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
        )

        sorted_rolling_skewness_df: DataFrameFloat = sort_dataframe(
            df=rolling_skewness_df,
            ascending=True
        )

        return Widgets.curves(
            x_values=sorted_rolling_skewness_df.dates,
            y_values=sorted_rolling_skewness_df,
            title="Rolling Smoothed Skewness"
        )

        
    @staticmethod
    def plot_overall_returns(returns_df: DataFrameFloat) -> go.Figure:
        total_returns_series = SeriesFloat(
            data=Computations.calculate_total_returns(returns_array=returns_df.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_total_returns: SeriesFloat = sort_series(series=total_returns_series, ascending=True)

        return Widgets.bars(
            series=sorted_total_returns,
            title="Total Returns")

    @staticmethod
    def plot_overall_sharpe_ratio(returns_df: DataFrameFloat) -> go.Figure:
        sharpes_series = SeriesFloat(
            data=Computations.overall_sharpe_ratio(returns_array=returns_df.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_sharpes_series: SeriesFloat = sort_series(series=sharpes_series, ascending=True)
        return Widgets.bars(
            series=sorted_sharpes_series, 
            title="Sharpe Ratio")

    @staticmethod
    def plot_overall_volatility(returns_df: DataFrameFloat) -> go.Figure:
        overall_vol_series = SeriesFloat(
            data=Computations.overall_volatility_annualized(array=returns_df.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_volatility: SeriesFloat = sort_series(series=overall_vol_series, ascending=True)

        return Widgets.bars(
            series=sorted_volatility, 
            title="Volatility %")

    @staticmethod
    def plot_overall_average_drawdown(returns_df: DataFrameFloat) -> go.Figure:
        rolling_dd = DataFrameFloat(
            data=Computations.calculate_rolling_drawdown(returns_array=returns_df.nparray, length=returns_df.shape[0]),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
            )
        drawdowns_series = SeriesFloat(
            data=Computations.calculate_overall_mean(array=rolling_dd.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_drawdowns: SeriesFloat = sort_series(series=drawdowns_series, ascending=True)

        return Widgets.bars(
            series=sorted_drawdowns, 
            title="Average Drawdowns %")
    @staticmethod
    def plot_overall_average_correlation(returns_df: DataFrameFloat) -> go.Figure:
        overall_average_corr = SeriesFloat(
            data=Computations.calculate_overall_average_correlation(returns_array=returns_df.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_overall_average_corr: SeriesFloat = sort_series(series=overall_average_corr, ascending=True)
        return Widgets.bars(
            series=sorted_overall_average_corr, 
            title="Overall Average Correlation")

    @staticmethod
    def plot_overall_monthly_skew(returns_df: DataFrameFloat) -> go.Figure:

        skew_series: SeriesFloat = SeriesFloat(
            data=Computations.calculate_overall_monthly_skewness(returns_array=returns_df.nparray),
            index=convert_multiindex_to_labels(df=returns_df)
            )
        sorted_skew_series: SeriesFloat = sort_series(series=skew_series, ascending=True)
        return Widgets.bars(
            series=sorted_skew_series, 
            title="Monthly Skew")
    @staticmethod
    def plot_returns_distribution_violin(returns_df: DataFrameFloat, limit:float=0.05) -> go.Figure:

        formatted_pct_returns_df = DataFrameFloat(
            data=format_returns(returns_array=returns_df.nparray, limit=limit),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
            )

        return Widgets.violin(
            data=formatted_pct_returns_df,
            title="Violin of % Returns Distribution")
    @staticmethod
    def plot_returns_distribution_histogram(returns_df: DataFrameFloat, limit: float = 0.05) -> go.Figure:

        formatted_pct_returns_df = DataFrameFloat(
            data=format_returns(returns_array=returns_df.nparray, limit=limit),
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
            )

        return Widgets.histogram(
            data=formatted_pct_returns_df,
            title="Histogram of % Returns Distribution")
    @staticmethod
    def plot_correlation_heatmap(returns_df: DataFrameFloat) -> go.Figure:
        correlation_matrix: ArrayFloat = Computations.calculate_correlation_matrix(returns_array=returns_df.nparray)
        filled_correlation_matrix: ArrayFloat = fill_correlation_matrix(corr_matrix=correlation_matrix)
        labels_list: list[str] = convert_multiindex_to_labels(df=returns_df)

        return Widgets.heatmap(
            z_values=filled_correlation_matrix,
            x_labels=labels_list,
            y_labels=labels_list,
            title="Correlation Matrix")
    @staticmethod
    def plot_clusters_icicle(
        returns_df: DataFrameFloat, 
        max_clusters: int = 4, 
        max_sub_clusters: int = 2
        ) -> go.Figure:
        
        renamed_returns_df = DataFrameFloat(
            data=returns_df.nparray,
            index=returns_df.dates,
            columns=convert_multiindex_to_labels(df=returns_df)
            )
        clusters_dict: DictVariableDepth = generate_static_clusters(
            returns_df=renamed_returns_df, 
            max_clusters=max_clusters, 
            max_subclusters=max_sub_clusters
            )
        labels, parents = prepare_sunburst_data(cluster_dict=clusters_dict)

        return Widgets.icicle(
            labels=labels, 
            parents=parents, 
            title="Clusters")