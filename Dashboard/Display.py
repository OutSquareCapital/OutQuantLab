import pandas as pd
import Dashboard.Transformations as Transformations
import Dashboard.Widgets as Widgets 
import Dashboard.Computations as Computations
from Portfolio import generate_static_clusters

def plot_equity(returns_df: pd.DataFrame):

    equity_curves = Computations.calculate_equity_curves_df(returns_df)
    
    sorted_equity_curves = Transformations.sort_dataframe(equity_curves, 
                                                            use_final=True,
                                                            ascending=True)

    Widgets.curves(x_values=sorted_equity_curves.index,
                   y_values=sorted_equity_curves,
                   title="Equity Curves", 
                   xlabel='Date', 
                   ylabel='Equity', 
                   log_scale=True)

def plot_rolling_volatility(returns_df: pd.DataFrame):

    rolling_volatility_df = Computations.calculate_rolling_volatility(returns_df)
    sorted_rolling_volatility_df = Transformations.sort_dataframe(rolling_volatility_df,
                                                                  ascending=False)

    Widgets.curves(x_values=sorted_rolling_volatility_df.index,
                   y_values=sorted_rolling_volatility_df, 
                   title="Rolling Volatility", 
                   xlabel='Date', 
                   ylabel='Rolling Volatility (%)', 
                   add_zero_line=True)

def plot_drawdowns(returns_df: pd.DataFrame):
    
    drawdowns = Computations.calculate_drawdown(returns_df)
    sorted_drawdowns = Transformations.sort_dataframe(drawdowns,
                                                      ascending=True)

    Widgets.curves(x_values=sorted_drawdowns.index, 
                   y_values=sorted_drawdowns, 
                   title="Drawdowns",
                   xlabel="Date",
                   ylabel="Drawdown (%)", 
                   add_zero_line=True)

def plot_rolling_sharpe_ratio(returns_df: pd.DataFrame):

    rolling_sharpe_ratio_df = Computations.calculate_rolling_sharpe_ratio(returns_df)
    sorted_rolling_sharpe_ratio_df = Transformations.sort_dataframe(rolling_sharpe_ratio_df,
                                                                    ascending=True)

    Widgets.curves(x_values=sorted_rolling_sharpe_ratio_df.index,
                   y_values=sorted_rolling_sharpe_ratio_df, 
                   title="Rolling Sharpe Ratios", 
                   xlabel='Date', 
                   ylabel='Rolling Sharpe Ratio', 
                   add_zero_line=True)

def plot_overall_sharpe_ratio(daily_returns: pd.DataFrame):

    sharpe_ratios = Computations.calculate_overall_sharpe_ratio(daily_returns).squeeze()
    sorted_sharpe_ratios = Transformations.sort_series(sharpe_ratios, ascending=True)

    Widgets.bars(series=sorted_sharpe_ratios, 
                 title="Sharpe Ratios", 
                 xlabel="Strats", 
                 ylabel="Sharpe Ratio")

def plot_overall_sortino_ratios(returns_df: pd.DataFrame):

    sortino_ratios = Computations.calculate_overall_sortino_ratio(returns_df).squeeze()
    sorted_sortino_ratios = Transformations.sort_series(sortino_ratios, ascending=True)

    Widgets.bars(series=sorted_sortino_ratios, 
                 title="Sortino Ratios", 
                 xlabel="Strats", 
                 ylabel="Sortino Ratio")

def plot_average_drawdown(returns_df: pd.DataFrame):

    drawdowns = Computations.calculate_average_drawdown(returns_df)
    sorted_drawdowns = Transformations.sort_series(drawdowns, ascending=True)

    Widgets.bars(series=sorted_drawdowns, 
                 title="Mean Drawdowns", 
                 xlabel="Strats", 
                 ylabel="Mean Drawdown (%)")

def plot_average_inverted_correlation(returns_df: pd.DataFrame):

    average_correlations = Computations.calculate_average_correlation(returns_df).squeeze() * -1
    sorted_correlations = Transformations.sort_series(average_correlations, ascending=True)

    Widgets.bars(series=sorted_correlations, 
                 title="Average Inverted Correlation",
                 xlabel="Strats", 
                 ylabel="Average Inverted Correlation")

def plot_overall_monthly_skew(returns_df: pd.DataFrame):

    skew_series = Computations.calculate_overall_monthly_skew(returns_df)
    sorted_skew_series = Transformations.sort_series(skew_series, ascending=True)

    Widgets.bars(series=sorted_skew_series, 
                 title="Monthly Skew", 
                 xlabel="Strats", 
                 ylabel="Skew")
    
def plot_overall_sharpe_correlation_ratio(returns_df: pd.DataFrame):

    sharpe_correlation_ratio = Computations.calculate_overall_sharpe_correlation_ratio(returns_df)['Sharpe/AvgCorrelation']
    sorted_sharpe_correlation_ratio = Transformations.sort_series(sharpe_correlation_ratio, ascending=True)

    Widgets.bars(series=sorted_sharpe_correlation_ratio, 
                 title="Sharpe Ratio Rank / Average Correlation Rank", 
                 xlabel="Strats", 
                 ylabel="Sharpe / Avg Correlation")

def plot_returns_distribution_violin(returns_df: pd.DataFrame, limit:float=0.05):

    pct_returns = Computations.format_returns(returns_df, limit)

    Widgets.violin(
        data=pct_returns,
        title="Violin Plot of % Returns Distribution",
        xlabel="Assets",
        ylabel="% Returns")

def plot_returns_distribution_histogram(returns_df: pd.DataFrame, limit: float = 0.05):

    formatted_returns_df = Computations.format_returns(returns_df, limit=limit)

    Widgets.histogram(
        data=formatted_returns_df,
        title="Histogram Plot of % Returns Distribution",
        xlabel="Returns %",
        ylabel="Frequency")

def plot_correlation_heatmap(returns_df: pd.DataFrame):

    correlation_matrix = Computations.calculate_overall_correlation_matrix(returns_df)

    Widgets.heatmap(
        z_values=correlation_matrix.values,
        x_labels=correlation_matrix.columns,
        y_labels=correlation_matrix.columns,
        title="Correlation Matrix",
        colorbar_title="Correlation")

def plot_sharpe_ratio_heatmap(returns_df: pd.DataFrame, param1: str, param2: str):

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)

    X, Y, Z = Transformations.convert_params_to_3d(sharpe_ratios_df, param1, param2)

    Widgets.heatmap(z_values=Z,
                    x_labels=X[0],
                    y_labels=Y[:, 0],
                    title=f"Sharpe Ratios for {param1} and {param2}",
                    colorbar_title="Sharpe Ratio")

def plot_overall_sharpe_ratio_3d_scatter(returns_df: pd.DataFrame, params: list):

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)

    x_vals, y_vals, z_vals, sharpe_means = Transformations.convert_params_to_4d(sharpe_ratios_df, params)

    Widgets.scatter_3d(x_vals=x_vals, 
                       y_vals=y_vals, 
                       z_vals=z_vals, 
                       values=sharpe_means, 
                       params=params,
                       title="Scatter Plot 3D")

def plot_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):

    clusters_dict = generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)

    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)

    Widgets.treemap(labels=labels, 
                    parents=parents, 
                    title="Clusters")