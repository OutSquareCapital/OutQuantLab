from Utilitary import ArrayFloat, DataFrameFloat, DictVariableDepth, SeriesFloat
import Dashboard.Transformations as Transformations
import Dashboard.Widgets as Widgets 
import Metrics as Computations
from ConfigClasses import generate_static_clusters, sort_correlation_matrix
from collections.abc import Callable
import plotly.graph_objects as go # type: ignore
from dataclasses import dataclass
from Indicators.Indics_Raw import smoothed_skewness

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
        all_dashboards:dict[str, DashboardPlot] = {}
        for name, func in globals().items():
            if callable(func) and name.startswith("plot_"):
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

    def plot(self, dashboard_name: str, global_plot:bool = False) -> go.Figure:
        
        dashboard: DashboardPlot = self.all_dashboards[dashboard_name]
        portfolio: DataFrameFloat = self.global_portfolio if global_plot else self.sub_portfolios

        if dashboard.length_required:
            return dashboard.func(portfolio, length=self.length)
        return dashboard.func(portfolio)

def plot_equity(returns_df: DataFrameFloat) -> go.Figure:
    
    equity_curves_df = DataFrameFloat(
        data=Computations.calculate_equity_curves(returns_array=returns_df.nparray),
        index=returns_df.dates,
        columns=returns_df.columns
        )

    sorted_equity_curves: DataFrameFloat = Transformations.sort_dataframe(
        equity_curves_df,
        use_final=True,
        ascending=True)
    
    sorted_equity_curves=Transformations.convert_dataframe_multiindex_labels(sorted_equity_curves)

    return Widgets.curves(
        x_values=sorted_equity_curves.dates,
        y_values=sorted_equity_curves,
        title="Equity Curve", 
        log_scale=True)

def plot_rolling_volatility(returns_df: DataFrameFloat) -> go.Figure:

    rolling_volatility_df = DataFrameFloat(
        data=Computations.hv_composite(returns_array=returns_df.nparray),
        index=returns_df.dates,
        columns=returns_df.columns
        )

    sorted_rolling_volatility_df: DataFrameFloat = Transformations.sort_dataframe(
        df=rolling_volatility_df,
        ascending=False)

    sorted_rolling_volatility_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_volatility_df)

    return Widgets.curves(
        x_values=sorted_rolling_volatility_df.dates,
        y_values=sorted_rolling_volatility_df, 
        title="Rolling Volatility %")

def plot_rolling_drawdown(returns_df: DataFrameFloat, length: int) -> go.Figure:
    
    drawdowns_df = DataFrameFloat(
        data=Computations.calculate_rolling_drawdown(returns_array=returns_df.nparray, length=length),
        index=returns_df.dates,
        columns=returns_df.columns
        )
    
    sorted_drawdowns: DataFrameFloat = Transformations.sort_dataframe(
        df=drawdowns_df,
        ascending=True)
    sorted_drawdowns=Transformations.convert_dataframe_multiindex_labels(sorted_drawdowns)

    return Widgets.curves(
        x_values=sorted_drawdowns.dates, 
        y_values=sorted_drawdowns, 
        title="Rolling Drawdown %")

def plot_rolling_sharpe_ratio(returns_df: DataFrameFloat, length: int) -> go.Figure:

    rolling_sharpe_ratio_df = DataFrameFloat(
        data=Computations.rolling_sharpe_ratios(returns_array=returns_df.nparray, length=length, min_length=length),
        index=returns_df.dates,
        columns=returns_df.columns)

    sorted_rolling_sharpe_ratio_df: DataFrameFloat = Transformations.sort_dataframe(
        df=rolling_sharpe_ratio_df,
        ascending=True)
    sorted_rolling_sharpe_ratio_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_sharpe_ratio_df)
    return Widgets.curves(
        x_values=sorted_rolling_sharpe_ratio_df.dates,
        y_values=sorted_rolling_sharpe_ratio_df, 
        title="Rolling Sharpe Ratio")
    
def plot_rolling_smoothed_skewness(returns_df: DataFrameFloat, length: int) -> go.Figure:
    rolling_skewness_df = DataFrameFloat(
        data=smoothed_skewness(returns_array=returns_df.nparray, LenSmooth=length, LenSkew=length),
        index=returns_df.dates,
        columns=returns_df.columns
        )

    sorted_rolling_skewness_df: DataFrameFloat = Transformations.sort_dataframe(
        df=rolling_skewness_df,
        ascending=True)

    sorted_rolling_skewness_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_skewness_df)
    return Widgets.curves(
        x_values=sorted_rolling_skewness_df.dates,
        y_values=sorted_rolling_skewness_df, 
        title="Rolling Smoothed Skewnesss")

def plot_rolling_average_inverted_correlation(returns_df: DataFrameFloat, length: int) -> go.Figure:
    rolling_correlations: DataFrameFloat = Computations.calculate_rolling_average_correlation(returns_df=returns_df, length=length)
    inverted_correlations: DataFrameFloat = rolling_correlations * -1
    sorted_correlations: DataFrameFloat = Transformations.sort_dataframe(df=inverted_correlations, ascending=True)
    sorted_correlations=Transformations.convert_dataframe_multiindex_labels(df=sorted_correlations)
    
    return Widgets.curves(
        x_values=sorted_correlations.dates,
        y_values=sorted_correlations,
        title=f"Rolling Average Inverted Correlation"
    )

def plot_overall_returns(returns_df: DataFrameFloat) -> go.Figure:
    total_returns_series = SeriesFloat(data=Computations.calculate_total_returns(returns_array=returns_df.nparray),index=returns_df.columns)
    sorted_total_returns: SeriesFloat = Transformations.sort_series(series=total_returns_series, ascending=True)
    return Widgets.bars(
        series=sorted_total_returns,
        title="Total Returns")

def plot_overall_sharpe_ratio(returns_df: DataFrameFloat) -> go.Figure:
    sharpes_series= SeriesFloat(data=Computations.overall_sharpe_ratio(returns_array=returns_df.nparray),index=returns_df.columns)
    sorted_sharpes_series: SeriesFloat = Transformations.sort_series(series=sharpes_series, ascending=True)
    return Widgets.bars(
        series=sorted_sharpes_series, 
        title="Sharpe Ratio")

def plot_overall_volatility(returns_df: DataFrameFloat) -> go.Figure:
    overall_vol_series = SeriesFloat(data=Computations.overall_volatility_annualized(array=returns_df.nparray),index=returns_df.columns)
    sorted_volatility: SeriesFloat = Transformations.sort_series(series=overall_vol_series, ascending=True)
    return Widgets.bars(
        series=sorted_volatility, 
        title="Volatility %")

def plot_overall_average_drawdown(returns_df: DataFrameFloat, length: int) -> go.Figure:
    rolling_dd: ArrayFloat = Computations.calculate_rolling_drawdown(returns_array=returns_df.nparray, length=length)
    drawdowns_series = SeriesFloat(data=Computations.calculate_overall_mean(array=rolling_dd),index=returns_df.columns)
    sorted_drawdowns: SeriesFloat = Transformations.sort_series(series=drawdowns_series, ascending=True)
    return Widgets.bars(
        series=sorted_drawdowns, 
        title="Average Drawdowns %")

def plot_overall_average_inverted_correlation(returns_df: DataFrameFloat) -> go.Figure:
    average_correlations: SeriesFloat = Computations.calculate_overall_average_correlation(returns_df=returns_df)
    inverted_average_correlations = SeriesFloat(data=average_correlations * -1)
    sorted_correlations: SeriesFloat = Transformations.sort_series(series=inverted_average_correlations, ascending=True)
    sorted_correlations=Transformations.convert_series_multiindex_labels(series=sorted_correlations)
    return Widgets.bars(
        series=sorted_correlations, 
        title="Average Inverted Correlation")

def plot_overall_monthly_skew(returns_df: DataFrameFloat) -> go.Figure:

    skew_series: SeriesFloat = SeriesFloat(
        data=Computations.calculate_overall_monthly_skewness(returns_array=returns_df.nparray),
        index=returns_df.columns
        )
    sorted_skew_series: SeriesFloat = Transformations.sort_series(series=skew_series, ascending=True)
    return Widgets.bars(
        series=sorted_skew_series, 
        title="Monthly Skew")

def plot_returns_distribution_violin(returns_df: DataFrameFloat, limit:float=0.05) -> go.Figure:

    pct_returns: DataFrameFloat = Transformations.format_returns(returns_df=returns_df, limit=limit)
    pct_returns = Transformations.convert_dataframe_multiindex_labels(df=pct_returns)
    return Widgets.violin(
        data=pct_returns,
        title="Violin of % Returns Distribution")

def plot_returns_distribution_histogram(returns_df: DataFrameFloat, limit: float = 0.05) -> go.Figure:

    formatted_returns_df: DataFrameFloat = Transformations.format_returns(returns_df=returns_df, limit=limit)
    formatted_returns_df = Transformations.convert_dataframe_multiindex_labels(df=formatted_returns_df)
    return Widgets.histogram(
        data=formatted_returns_df,
        title="Histogram of % Returns Distribution")

def plot_correlation_heatmap(returns_df: DataFrameFloat) -> go.Figure:

    correlation_matrix: DataFrameFloat = Computations.calculate_correlation_matrix(returns_df=returns_df)
    sorted_correlation_matrix: DataFrameFloat = sort_correlation_matrix(corr_matrix=correlation_matrix)
    sorted_correlation_matrix = Transformations.convert_dataframe_multiindex_labels(df=sorted_correlation_matrix)
    return Widgets.heatmap(
        z_values=sorted_correlation_matrix.nparray,
        x_labels=sorted_correlation_matrix.columns.to_list(),
        y_labels=sorted_correlation_matrix.columns.to_list(),
        title="Correlation Matrix")

def plot_clusters_icicle(
    returns_df: DataFrameFloat, 
    max_clusters: int = 4, 
    max_sub_clusters: int = 2, 
    max_sub_sub_clusters: int = 1
    ) -> go.Figure:
    
    renamed_returns_df: DataFrameFloat=Transformations.convert_dataframe_multiindex_labels(returns_df)
    clusters_dict: DictVariableDepth = generate_static_clusters(
        returns_df=renamed_returns_df, 
        max_clusters=max_clusters, 
        max_subclusters=max_sub_clusters, 
        max_subsubclusters=max_sub_sub_clusters
        )
    labels, parents = Transformations.prepare_sunburst_data(cluster_dict=clusters_dict)

    return Widgets.icicle(
        labels=labels, 
        parents=parents, 
        title="Clusters")