import pandas as pd
import Dashboard.Transformations as Transformations
import Dashboard.Widgets as Widgets 
import Dashboard.Computations as Computations
from Portfolio import generate_static_clusters
from collections.abc import Callable
import plotly.graph_objects as go
from dataclasses import dataclass

@dataclass()
class DashboardPlot:
    name: str
    func: Callable
    category: str
    length_required: bool

class DashboardsCollection:
    def __init__(self, length):
        self.global_portfolio: pd.DataFrame
        self.sub_portfolios: pd.DataFrame
        self.length: int = length
        self.metrics: list[float]
        self.all_dashboards: dict[str, DashboardPlot] = self.__initialize_dashboards()

    def __initialize_dashboards(self) -> dict[str, DashboardPlot]:
        all_dashboards = {}
        for name, func in globals().items():
            if callable(func) and name.startswith("plot_"):
                formatted_name = name[5:].replace("_", " ").title()
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

    def calculate_metrics(self) -> list[float]:
        metric_functions: list[Callable] = [
            Computations.calculate_overall_returns,
            Computations.calculate_overall_sharpe_ratio,
            Computations.calculate_overall_max_drawdown,
            Computations.calculate_overall_volatility,
            Computations.calculate_overall_monthly_skew,
        ]

        return [round(func(self.global_portfolio).item(), 2) for func in metric_functions]

    def plot(self, dashboard_name: str, global_plot:bool = False) -> go.Figure:
        
        dashboard = self.all_dashboards[dashboard_name]
        portfolio = self.global_portfolio if global_plot else self.sub_portfolios

        if dashboard.length_required:
            return dashboard.func(portfolio, length=self.length)
        return dashboard.func(portfolio)

def plot_equity(returns_df: pd.DataFrame) -> go.Figure:

    equity_curves = Computations.calculate_equity_curves_df(returns_df)
    
    sorted_equity_curves = Transformations.sort_dataframe(
        equity_curves, 
        use_final=True,
        ascending=True)
    
    sorted_equity_curves=Transformations.convert_dataframe_multiindex_labels(sorted_equity_curves)

    return Widgets.curves(
        x_values=sorted_equity_curves.index,
        y_values=sorted_equity_curves,
        title="Equity Curve", 
        log_scale=True)

def plot_rolling_volatility(returns_df: pd.DataFrame) -> go.Figure:

    rolling_volatility_df = Computations.calculate_rolling_volatility(returns_df)
    sorted_rolling_volatility_df = Transformations.sort_dataframe(
        rolling_volatility_df,
        ascending=False)

    sorted_rolling_volatility_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_volatility_df)

    return Widgets.curves(
        x_values=sorted_rolling_volatility_df.index,
        y_values=sorted_rolling_volatility_df, 
        title="Rolling Volatility %")

def plot_rolling_drawdown(returns_df: pd.DataFrame, length: int) -> go.Figure:
    
    drawdowns = Computations.calculate_rolling_drawdown(returns_df, length)
    sorted_drawdowns = Transformations.sort_dataframe(
        drawdowns,
        ascending=True)
    sorted_drawdowns=Transformations.convert_dataframe_multiindex_labels(sorted_drawdowns)

    return Widgets.curves(
        x_values=sorted_drawdowns.index, 
        y_values=sorted_drawdowns, 
        title="Rolling Drawdown %")

def plot_rolling_sharpe_ratio(returns_df: pd.DataFrame, length: int) -> go.Figure:

    rolling_sharpe_ratio_df = Computations.calculate_rolling_sharpe_ratio(returns_df, length)
    sorted_rolling_sharpe_ratio_df = Transformations.sort_dataframe(
        rolling_sharpe_ratio_df,
        ascending=True)
    sorted_rolling_sharpe_ratio_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_sharpe_ratio_df)
    return Widgets.curves(
        x_values=sorted_rolling_sharpe_ratio_df.index,
        y_values=sorted_rolling_sharpe_ratio_df, 
        title="Rolling Sharpe Ratio")
    
def plot_rolling_smoothed_skewness(returns_df: pd.DataFrame, length: int) -> go.Figure:

    rolling_skewness_df = Computations.calculate_rolling_smoothed_skewness(returns_df, length)
    sorted_rolling_skewness_df = Transformations.sort_dataframe(
        rolling_skewness_df,
        ascending=True)
    sorted_rolling_skewness_df=Transformations.convert_dataframe_multiindex_labels(sorted_rolling_skewness_df)
    return Widgets.curves(
        x_values=sorted_rolling_skewness_df.index,
        y_values=sorted_rolling_skewness_df, 
        title="Rolling Smoothed Skewnesss")

def plot_rolling_average_inverted_correlation(returns_df: pd.DataFrame, length: int) -> go.Figure:
    
    rolling_correlations = Computations.calculate_rolling_average_correlation(returns_df, length)
    inverted_correlations = rolling_correlations * -1
    sorted_correlations = Transformations.sort_dataframe(inverted_correlations, ascending=True)
    sorted_correlations=Transformations.convert_dataframe_multiindex_labels(sorted_correlations)
    
    return Widgets.curves(
        x_values=sorted_correlations.index,
        y_values=sorted_correlations,
        title=f"Rolling Average Inverted Correlation"
    )

def plot_overall_returns(returns_df: pd.DataFrame) -> go.Figure:

    total_returns = Computations.calculate_overall_returns(returns_df)
    
    sorted_total_returns = Transformations.sort_series(
        total_returns, 
        ascending=True)
    sorted_total_returns=Transformations.convert_series_multiindex_labels(sorted_total_returns)

    return Widgets.bars(
        series=sorted_total_returns,
        title="Total Returns")

def plot_overall_sharpe_ratio(returns_df: pd.DataFrame) -> go.Figure:

    sharpe_ratios = Computations.calculate_overall_sharpe_ratio(returns_df)
    sorted_sharpe_ratios = Transformations.sort_series(sharpe_ratios, ascending=True)
    sorted_sharpe_ratios=Transformations.convert_series_multiindex_labels(sorted_sharpe_ratios)
    return Widgets.bars(
        series=sorted_sharpe_ratios, 
        title="Sharpe Ratio")

def plot_overall_volatility(returns_df: pd.DataFrame) -> go.Figure:

    volatility = Computations.calculate_overall_volatility(returns_df)
    sorted_volatility = Transformations.sort_series(volatility, ascending=True)
    sorted_volatility=Transformations.convert_series_multiindex_labels(sorted_volatility)
    return Widgets.bars(
        series=sorted_volatility, 
        title="Volatility %")
    
def plot_overall_average_drawdown(returns_df: pd.DataFrame, length: int) -> go.Figure:

    drawdowns = Computations.calculate_overall_average_drawdown(returns_df, length)
    sorted_drawdowns = Transformations.sort_series(drawdowns, ascending=True)
    sorted_drawdowns=Transformations.convert_series_multiindex_labels(sorted_drawdowns)
    return Widgets.bars(
        series=sorted_drawdowns, 
        title="Average Drawdowns %")

def plot_overall_average_inverted_correlation(returns_df: pd.DataFrame) -> go.Figure:

    average_correlations = Computations.calculate_overall_average_correlation(returns_df) * -1
    sorted_correlations = Transformations.sort_series(average_correlations, ascending=True)
    sorted_correlations=Transformations.convert_series_multiindex_labels(sorted_correlations)
    return Widgets.bars(
        series=sorted_correlations, 
        title="Average Inverted Correlation")

def plot_overall_monthly_skew(returns_df: pd.DataFrame) -> go.Figure:

    skew_series = Computations.calculate_overall_monthly_skew(returns_df)
    sorted_skew_series = Transformations.sort_series(skew_series, ascending=True)
    sorted_skew_series=Transformations.convert_series_multiindex_labels(sorted_skew_series)
    return Widgets.bars(
        series=sorted_skew_series, 
        title="Monthly Skew")

def plot_returns_distribution_violin(returns_df: pd.DataFrame, limit:float=0.05) -> go.Figure:

    pct_returns = Computations.format_returns(returns_df, limit)
    pct_returns = Transformations.convert_dataframe_multiindex_labels(pct_returns)
    return Widgets.violin(
        data=pct_returns,
        title="Violin of % Returns Distribution")

def plot_returns_distribution_histogram(returns_df: pd.DataFrame, limit: float = 0.05) -> go.Figure:

    formatted_returns_df = Computations.format_returns(returns_df, limit=limit)
    formatted_returns_df = Transformations.convert_dataframe_multiindex_labels(formatted_returns_df)
    return Widgets.histogram(
        data=formatted_returns_df,
        title="Histogram of % Returns Distribution")

def plot_correlation_heatmap(returns_df: pd.DataFrame) -> go.Figure:

    correlation_matrix = Computations.calculate_correlation_matrix(returns_df)
    sorted_correlation_matrix = Transformations.sort_correlation_matrix(correlation_matrix)
    sorted_correlation_matrix = Transformations.convert_dataframe_multiindex_labels(sorted_correlation_matrix)
    return Widgets.heatmap(
        z_values=sorted_correlation_matrix.values,
        x_labels=sorted_correlation_matrix.columns.to_list(),
        y_labels=sorted_correlation_matrix.columns.to_list(),
        title="Correlation Matrix")

def plot_clusters_icicle(returns_df: pd.DataFrame, max_clusters=4, max_sub_clusters=2, max_sub_sub_clusters=1) -> go.Figure:
    
    renamed_returns_df=Transformations.convert_dataframe_multiindex_labels(returns_df)
    clusters_dict = generate_static_clusters(renamed_returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)
    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)

    return Widgets.icicle(
        labels=labels, 
        parents=parents, 
        title="Clusters")

def plot_sharpe_ratio_heatmap(returns_df: pd.DataFrame, param1: str, param2: str) -> go.Figure:

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)
    sharpe_ratios_df=Transformations.convert_dataframe_multiindex_labels(sharpe_ratios_df)
    X, Y, Z = Transformations.convert_params_to_3d(sharpe_ratios_df, param1, param2)

    return Widgets.heatmap(
        z_values=Z,
        x_labels=X[0],
        y_labels=Y[:, 0].tolist(),
        title=f"Sharpe Ratios for {param1} and {param2}")

def plot_overall_sharpe_ratio_3d_scatter(returns_df: pd.DataFrame, params: list) -> go.Figure:

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)
    sharpe_ratios_df=Transformations.convert_dataframe_multiindex_labels(sharpe_ratios_df)
    x_vals, y_vals, z_vals, sharpe_means = Transformations.convert_params_to_4d(sharpe_ratios_df, params)

    return Widgets.scatter_3d(
        x_vals=x_vals, 
        y_vals=y_vals, 
        z_vals=z_vals, 
        values=sharpe_means, 
        params=params,
        title="Scatter Plot 3D")