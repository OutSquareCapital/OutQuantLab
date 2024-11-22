import pandas as pd
import Dashboard.Transformations as Transformations
import Dashboard.Widgets as Widgets 
import Dashboard.Computations as Computations

from Process_Data import equity_curves_calculs
from Portfolio import generate_static_clusters

def equity(returns_df: pd.DataFrame):

    equity_curves = equity_curves_calculs(returns_df)
    final_values = equity_curves.iloc[-1]
    sorted_columns = Transformations.sort_columns_by_metric(final_values, ascending=True)

    Widgets.curves(y_values=equity_curves[sorted_columns], 
                   x_values=equity_curves.index, 
                   title="Equity Curves", 
                   xlabel='Date', 
                   ylabel='Equity', 
                   log_scale=True)

def plot_final_equity_values(daily_returns: pd.DataFrame):

    final_equities_df = Computations.calculate_final_equity_values(daily_returns)
    sorted_columns = Transformations.sort_by_final_equity(final_equities_df)

    Widgets.curves(x_values=final_equities_df[sorted_columns], 
                   y_values=final_equities_df.index, 
                   title="Final Equity Value Starting Each Day", 
                   xlabel='Start Date', 
                   ylabel='Final Equity Value')

def volatility(daily_returns: pd.DataFrame, means=False):

    rolling_volatility_df = Computations.rolling_volatility_calculs(daily_returns, means)
    sorted_columns = Transformations.sort_columns_by_volatility(rolling_volatility_df)

    Widgets.curves(x_values=rolling_volatility_df[sorted_columns], 
                   y_values=daily_returns.index, 
                   title="Rolling Volatility", 
                   xlabel='Date', 
                   ylabel='Rolling Volatility (%)', 
                   add_zero_line=True)

def drawdowns(returns_df: pd.DataFrame):

    drawdowns = Computations.drawdowns_calculs(returns_df)
    sorted_columns = Transformations.sort_columns_by_drawdown(drawdowns)

    Widgets.curves(x_values=drawdowns[sorted_columns], 
                   y_values=returns_df.index, 
                   title="Drawdowns", 
                   xlabel="Date", 
                   ylabel="Drawdown (%)", 
                   add_zero_line=True)

def rolling_sharpe_ratio(daily_returns: pd.DataFrame):

    rolling_sharpe_ratio_df = Computations.rolling_sharpe_ratios_calculs(daily_returns)
    sorted_columns = Transformations.sort_sharpe_ratios(rolling_sharpe_ratio_df)

    Widgets.curves(x_values=rolling_sharpe_ratio_df[sorted_columns], 
                   y_values=daily_returns.index, 
                   title="Rolling Sharpe Ratios", 
                   xlabel='Date', 
                   ylabel='Rolling Sharpe Ratio', 
                   add_zero_line=True)


def max_drawdowns(equity_curves: pd.DataFrame):
    drawdowns = Computations.drawdowns_calculs(equity_curves)
    sorted_drawdowns = Transformations.sort_max_drawdowns(drawdowns)
    data = pd.DataFrame({'x': sorted_drawdowns.index, 'y': sorted_drawdowns.values})

    Widgets.bars(data=data, 
                 title="Max Drawdowns", 
                 xlabel="Strats", 
                 ylabel="Max Drawdown (%)")

def average_inverted_correlation_bar_chart(daily_returns: pd.DataFrame):
    average_correlations_df = Computations.average_correlation_calculs(daily_returns) * -1
    sorted_correlations = Transformations.sort_average_correlation(average_correlations_df)
    data = pd.DataFrame({'x': sorted_correlations.index, 'y': sorted_correlations['Average Correlation']})

    Widgets.bars(data=data, 
                 title="Average Inverted Correlation",
                 xlabel="Strats", 
                 ylabel="Average Inverted Correlation")


def overall_sharpe_ratios(daily_returns: pd.DataFrame):
    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)
    sorted_sharpe_ratios = sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=True)
    data = pd.DataFrame({'x': sorted_sharpe_ratios.index, 'y': sorted_sharpe_ratios['Sharpe Ratio']})

    Widgets.bars(data, 
                 title="Sharpe Ratios", 
                 xlabel="Strats", 
                 ylabel="Sharpe Ratio")

def overall_monthly_skew(daily_returns: pd.DataFrame):
    skew_series = Computations.overall_monthly_skew_calculs(daily_returns)
    sorted_skew_series = skew_series.sort_values(ascending=True)
    data = pd.DataFrame({'x': sorted_skew_series.index, 'y': sorted_skew_series.values})
    Widgets.bars(data, 
                 title="Monthly Skew", 
                 xlabel="Strats", 
                 ylabel="Skew")

def sortino_ratios(daily_returns: pd.DataFrame):
    sortino_ratios_df = Computations.overall_sortino_ratios_calculs(daily_returns)
    sorted_sortino_ratios = sortino_ratios_df.sort_values(by='Sortino Ratio', ascending=True)
    data = pd.DataFrame({'x': sorted_sortino_ratios.index, 'y': sorted_sortino_ratios['Sortino Ratio']})
    Widgets.bars(data, 
                 title="Sortino Ratios", 
                 xlabel="Strats", 
                 ylabel="Sortino Ratio")
    
def sharpe_correlation_ratio_bar_chart(daily_returns: pd.DataFrame):
    combined_df = Computations.calculate_sharpe_correlation_ratio(daily_returns)
    sorted_combined_df = combined_df.sort_values(by='Sharpe/AvgCorrelation', ascending=True)
    data = pd.DataFrame({'x': sorted_combined_df.index, 'y': sorted_combined_df['Sharpe/AvgCorrelation']})
    Widgets.bars(data, 
                 title="Sharpe Ratio Rank / Average Correlation Rank", 
                 xlabel="Strats", 
                 ylabel="Sharpe / Avg Correlation")




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

def plot_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):
    clusters_dict = generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)
    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)
    Widgets.treemap(labels, parents, "Visualisation des Clusters")
