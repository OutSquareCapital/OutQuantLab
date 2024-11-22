import numpy as np
import pandas as pd
import plotly.graph_objects as go

import Dashboard.Transformations as Transformations
import Dashboard.Common as Common
import Dashboard.Widgets as Widgets 
import Dashboard.Computations as Computations

from Process_Data import equity_curves_calculs
from Portfolio import generate_static_clusters

def equity(returns_df: pd.DataFrame):
    title = 'Equity Curves'
    xlabel = 'Date'
    ylabel = 'Equity'

    equity_curves = equity_curves_calculs(returns_df)
    final_values = equity_curves.iloc[-1]
    sorted_columns = Transformations.sort_columns_by_metric(final_values, ascending=True)
    colors = dict(zip(sorted_columns, Common.map_colors_to_columns(len(sorted_columns), sorted_columns)))

    Widgets.plot_curves(equity_curves[sorted_columns], equity_curves.index, colors, title, xlabel, ylabel, log_scale=True)

def plot_final_equity_values(daily_returns: pd.DataFrame):
    final_equities_df = Computations.calculate_final_equity_values(daily_returns)
    title = 'Final Equity Value Starting Each Day'
    xlabel = 'Start Date'
    ylabel = 'Final Equity Value'

    final_equity_means = final_equities_df.mean()
    final_equity_percentiles = final_equity_means.rank(pct=True)
    sorted_columns = final_equity_percentiles.sort_values(ascending=True).index

    colors = dict(zip(sorted_columns, Common.map_colors_to_columns(len(sorted_columns), sorted_columns)))

    Widgets.plot_curves(final_equities_df[sorted_columns], final_equities_df.index, colors, title, xlabel, ylabel)


def volatility(daily_returns: pd.DataFrame, means=False):
    rolling_volatility_df = Computations.rolling_volatility_calculs(daily_returns, means)
    title = 'Rolling Volatility'
    xlabel = 'Date'
    ylabel = 'Rolling Volatility (%)'

    rolling_volatility_means = rolling_volatility_df.mean()
    sorted_columns = Transformations.sort_columns_by_metric(rolling_volatility_means, ascending=True)
    colors = dict(zip(sorted_columns, Common.map_colors_to_columns(len(sorted_columns), sorted_columns)))

    Widgets.plot_curves(rolling_volatility_df[sorted_columns], daily_returns.index, colors, title, xlabel, ylabel, add_zero_line=True)

def drawdowns(returns_df: pd.DataFrame):
    drawdowns = Computations.drawdowns_calculs(returns_df)
    title = "Drawdowns"
    xlabel = "Date"
    ylabel = "Drawdown (%)"

    drawdown_means = drawdowns.mean()
    sorted_columns = Transformations.sort_columns_by_metric(drawdown_means, ascending=True)
    colors = dict(zip(sorted_columns, Common.map_colors_to_columns(len(sorted_columns), sorted_columns)))

    Widgets.plot_curves(drawdowns[sorted_columns], returns_df.index, colors, title, xlabel, ylabel, add_zero_line=True)

def rolling_sharpe_ratio(daily_returns: pd.DataFrame):
    rolling_sharpe_ratio_df = Computations.rolling_sharpe_ratios_calculs(daily_returns)
    title = 'Rolling Sharpe Ratios'
    xlabel = 'Date'
    ylabel = 'Rolling Sharpe Ratio'

    mean_sharpes = {column: np.nanmean(sharpe) for column, sharpe in rolling_sharpe_ratio_df.items()}
    sorted_columns = sorted(mean_sharpes, key=mean_sharpes.get, reverse=False)
    colors = dict(zip(sorted_columns, Common.map_colors_to_columns(len(sorted_columns), sorted_columns)))

    Widgets.plot_curves(rolling_sharpe_ratio_df[sorted_columns], daily_returns.index, colors, title, xlabel, ylabel, add_zero_line=True)


def max_drawdowns(equity_curves: pd.DataFrame):

    drawdowns = Computations.drawdowns_calculs(equity_curves)
    max_drawdowns = drawdowns.min(axis=0)
    sorted_max_drawdowns = max_drawdowns.sort_values(ascending=True)
    data = pd.DataFrame({'x': sorted_max_drawdowns.index, 'y': sorted_max_drawdowns.values})
    Widgets.bar_chart(data, "Max Drawdowns", "Strats", "Max Drawdown (%)")

def annual_returns(daily_returns: pd.DataFrame):
    annual_returns = Computations.annual_returns_calculs(daily_returns)

    title = 'Yearly Returns'
    Widgets.colored_table(annual_returns, 
                            title, 
                            sort_ascending=True, 
                            color_high_to_low=False)

def average_inverted_correlation_bar_chart(daily_returns: pd.DataFrame):
    average_correlations_df = Computations.average_correlation_calculs(daily_returns) * -1
    sorted_correlations = average_correlations_df.sort_values(by='Average Correlation', ascending=True)
    data = pd.DataFrame({'x': sorted_correlations.index, 'y': sorted_correlations['Average Correlation']})
    Widgets.bar_chart(data, "Average Inverted Correlation", "Strats", "Average Inverted Correlation")

def overall_sharpe_ratios(daily_returns: pd.DataFrame):
    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)
    sorted_sharpe_ratios = sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=True)
    data = pd.DataFrame({'x': sorted_sharpe_ratios.index, 'y': sorted_sharpe_ratios['Sharpe Ratio']})
    Widgets.bar_chart(data, "Sharpe Ratios", "Strats", "Sharpe Ratio")



def overall_monthly_skew(daily_returns: pd.DataFrame):
    skew_series = Computations.overall_monthly_skew_calculs(daily_returns)
    sorted_skew_series = skew_series.sort_values(ascending=True)
    data = pd.DataFrame({'x': sorted_skew_series.index, 'y': sorted_skew_series.values})
    Widgets.bar_chart(data, "Monthly Skew", "Strats", "Skew")

def sharpe_ratios_yearly_table(daily_returns: pd.DataFrame):

    sharpe_ratios_df = Computations.sharpe_ratios_yearly_calculs(daily_returns)

    title = 'Sharpe Ratios per year'
    
    Widgets.colored_table(sharpe_ratios_df, 
                            title, 
                            sort_ascending=True, 
                            color_high_to_low=False)

def sortino_ratios(daily_returns: pd.DataFrame):
    sortino_ratios_df = Computations.overall_sortino_ratios_calculs(daily_returns)
    sorted_sortino_ratios = sortino_ratios_df.sort_values(by='Sortino Ratio', ascending=True)
    data = pd.DataFrame({'x': sorted_sortino_ratios.index, 'y': sorted_sortino_ratios['Sortino Ratio']})
    Widgets.bar_chart(data, "Sortino Ratios", "Strats", "Sortino Ratio")

def returns_distribution(daily_returns: pd.DataFrame, freq: str = 'H'):
    title = 'Histogram of Strategy % Returns Distribution'
    xlabel = 'Strategy % Returns'
    ylabel = 'Frequency'
    Widgets.histogram(daily_returns, title, xlabel, ylabel)

def sharpe_ratios_3d_scatter_plot(daily_returns: pd.DataFrame, params: list):
    x_vals, y_vals, z_vals, sharpe_means = Transformations.convert_params_to_4d(daily_returns, params)
    Widgets.scatter_3d(x_vals, y_vals, z_vals, sharpe_means, params, "Scatter Plot 3D")

def sharpe_ratios_heatmap(daily_returns: pd.DataFrame, param1: str, param2: str):
    X, Y, Z = Transformations.convert_params_to_3d(daily_returns, param1, param2)
    Widgets.heatmap(
        z_values=Z,
        x_labels=X[0].tolist(),  # Les valeurs X en liste
        y_labels=Y[:, 0].tolist(),  # Les valeurs Y en liste
        title=f"Heatmap of Sharpe Ratios for {param1} and {param2}",
        colorbar_title="Sharpe Ratio"
    )

def correlation_heatmap(daily_returns: pd.DataFrame):
    correlation_matrix = daily_returns.corr()
    Widgets.heatmap(
        z_values=correlation_matrix.values,
        x_labels=daily_returns.columns.tolist(),
        y_labels=daily_returns.columns.tolist(),
        title="Correlation Matrix",
        colorbar_title="Correlation"
    )

def sharpe_correlation_ratio_bar_chart(daily_returns: pd.DataFrame):
    combined_df = Computations.calculate_sharpe_correlation_ratio(daily_returns)
    sorted_combined_df = combined_df.sort_values(by='Sharpe/AvgCorrelation', ascending=True)
    data = pd.DataFrame({'x': sorted_combined_df.index, 'y': sorted_combined_df['Sharpe/AvgCorrelation']})
    Widgets.bar_chart(data, "Sharpe Ratio Rank / Average Correlation Rank", "Strats", "Sharpe / Avg Correlation")

def plot_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):
    clusters_dict = generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)
    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)
    Widgets.treemap(labels, parents, "Visualisation des Clusters")
