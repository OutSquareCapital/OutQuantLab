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
                   ylabel='Rolling Volatility (%)')

def plot_rolling_drawdown(returns_df: pd.DataFrame, length: int):
    
    drawdowns = Computations.calculate_rolling_drawdown(returns_df, length)
    sorted_drawdowns = Transformations.sort_dataframe(drawdowns,
                                                      ascending=True)

    Widgets.curves(x_values=sorted_drawdowns.index, 
                   y_values=sorted_drawdowns, 
                   title="Drawdowns",
                   xlabel="Date",
                   ylabel="Drawdown (%)")

def plot_rolling_sharpe_ratio(returns_df: pd.DataFrame, length: int):

    rolling_sharpe_ratio_df = Computations.calculate_rolling_sharpe_ratio(returns_df, length)
    sorted_rolling_sharpe_ratio_df = Transformations.sort_dataframe(rolling_sharpe_ratio_df,
                                                                    ascending=True)

    Widgets.curves(x_values=sorted_rolling_sharpe_ratio_df.index,
                   y_values=sorted_rolling_sharpe_ratio_df, 
                   title="Rolling Sharpe Ratios", 
                   xlabel='Date', 
                   ylabel='Rolling Sharpe Ratio', 
                   zero_line=True)
    
def plot_rolling_smoothed_skewness(returns_df: pd.DataFrame, length: int):

    rolling_skewness_df = Computations.calculate_rolling_smoothed_skewness(returns_df, length)
    sorted_rolling_skewness_df = Transformations.sort_dataframe(rolling_skewness_df,
                                                                    ascending=True)

    Widgets.curves(x_values=sorted_rolling_skewness_df.index,
                   y_values=sorted_rolling_skewness_df, 
                   title="Rolling Smoothed Skewnesss", 
                   xlabel='Date', 
                   ylabel='Rolling Skewness', 
                   zero_line=True)
    
def plot_rolling_average_inverted_correlation(returns_df: pd.DataFrame, length: int):
    rolling_correlations = Computations.calculate_rolling_average_correlation(returns_df, length)

    inverted_correlations = rolling_correlations * -1

    sorted_correlations = Transformations.sort_dataframe(inverted_correlations, ascending=True)

    Widgets.curves(
        x_values=sorted_correlations.index,
        y_values=sorted_correlations,
        title=f"Rolling Average Inverted Correlation",
        xlabel="Date",
        ylabel="Inverted Correlation",
        zero_line=True
    )


def plot_overall_sharpe_ratio(daily_returns: pd.DataFrame):

    sharpe_ratios = Computations.calculate_overall_sharpe_ratio(daily_returns).squeeze()
    sorted_sharpe_ratios = Transformations.sort_series(sharpe_ratios, ascending=True)

    Widgets.bars(series=sorted_sharpe_ratios, 
                 title="Sharpe Ratios", 
                 xlabel="Strats", 
                 ylabel="Sharpe Ratio")

def plot_overall_volatility(daily_returns: pd.DataFrame):

    volatility = Computations.calculate_overall_volatility(daily_returns).squeeze()
    sorted_volatility = Transformations.sort_series(volatility, ascending=True)

    Widgets.bars(series=sorted_volatility, 
                 title="Volatility", 
                 xlabel="Strats", 
                 ylabel="Volatility %")
    
def plot_overall_average_drawdown(returns_df: pd.DataFrame, length: int):

    drawdowns = Computations.calculate_overall_average_drawdown(returns_df, length).squeeze()
    sorted_drawdowns = Transformations.sort_series(drawdowns, ascending=True)

    Widgets.bars(series=sorted_drawdowns, 
                 title="Average Drawdowns", 
                 xlabel="Strats", 
                 ylabel="Average Drawdown (%)")

def plot_overall_average_inverted_correlation(returns_df: pd.DataFrame):

    average_correlations = Computations.calculate_overall_average_correlation(returns_df).squeeze() * -1
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
    sorted_correlation_matrix = Transformations.sort_correlation_matrix(correlation_matrix)

    Widgets.heatmap(
        z_values=sorted_correlation_matrix.values,
        x_labels=sorted_correlation_matrix.columns,
        y_labels=sorted_correlation_matrix.columns,
        title="Correlation Matrix")

def plot_clusters_icicle(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):
    
    clusters_dict = generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)
    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)

    Widgets.icicle(labels=labels, 
                   parents=parents, 
                   title="Clusters")

def plot_sharpe_ratio_heatmap(returns_df: pd.DataFrame, param1: str, param2: str):

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)

    X, Y, Z = Transformations.convert_params_to_3d(sharpe_ratios_df, param1, param2)

    Widgets.heatmap(z_values=Z,
                    x_labels=X[0],
                    y_labels=Y[:, 0],
                    title=f"Sharpe Ratios for {param1} and {param2}")

def plot_overall_sharpe_ratio_3d_scatter(returns_df: pd.DataFrame, params: list):

    sharpe_ratios_df = Computations.calculate_overall_sharpe_ratio(returns_df)

    x_vals, y_vals, z_vals, sharpe_means = Transformations.convert_params_to_4d(sharpe_ratios_df, params)

    Widgets.scatter_3d(x_vals=x_vals, 
                       y_vals=y_vals, 
                       z_vals=z_vals, 
                       values=sharpe_means, 
                       params=params,
                       title="Scatter Plot 3D")



def generate_dashboard_plots(
    test_returns_df: pd.DataFrame,
    raw_adjusted_returns_df: pd.DataFrame,
    limit: float = 0.01,
    rolling_window: int = 1250,
    cluster_params: tuple[int, int, int] = (6, 2, 1),
    scatter_params: list[str] = None,
    equity: bool = False,
    rolling_sharpe_ratio: bool = False,
    rolling_drawdown: bool = False,
    rolling_smoothed_skewness: bool = False,
    rolling_average_inverted_correlation: bool = False,
    rolling_volatility: bool = False,
    overall_sharpe_ratio: bool = False,
    overall_average_drawdown: bool = False,
    overall_monthly_skew: bool = False,
    overall_average_inverted_correlation: bool = False,
    overall_volatility: bool = False,
    returns_distribution_violin: bool = False,
    returns_distribution_histogram: bool = False,
    correlation_heatmap: bool = False,
    clusters_icicle: bool = False,
    sharpe_ratio_heatmap: bool = False,
    overall_sharpe_ratio_3d_scatter: bool = False,
):
    if equity:
        plot_equity(test_returns_df)
    
    if rolling_sharpe_ratio:
        plot_rolling_sharpe_ratio(test_returns_df, rolling_window)
    
    if rolling_drawdown:
        plot_rolling_drawdown(test_returns_df, rolling_window)
    
    if rolling_smoothed_skewness:
        plot_rolling_smoothed_skewness(test_returns_df, rolling_window)
    
    if rolling_average_inverted_correlation:
        plot_rolling_average_inverted_correlation(test_returns_df, rolling_window)
    
    if rolling_volatility:
        plot_rolling_volatility(test_returns_df)
    
    if overall_sharpe_ratio:
        plot_overall_sharpe_ratio(test_returns_df)
    
    if overall_average_drawdown:
        plot_overall_average_drawdown(test_returns_df, rolling_window)
    
    if overall_monthly_skew:
        plot_overall_monthly_skew(test_returns_df)
    
    if overall_average_inverted_correlation:
        plot_overall_average_inverted_correlation(test_returns_df)
    
    if overall_volatility:
        plot_overall_volatility(test_returns_df)
    
    if returns_distribution_violin:
        plot_returns_distribution_violin(test_returns_df, limit=limit)
    
    if returns_distribution_histogram:
        plot_returns_distribution_histogram(test_returns_df, limit=limit)
    
    if correlation_heatmap:
        plot_correlation_heatmap(test_returns_df)
    
    if clusters_icicle:
        plot_clusters_icicle(test_returns_df, *cluster_params)
    
    if sharpe_ratio_heatmap:
        plot_sharpe_ratio_heatmap(raw_adjusted_returns_df, 'LenST', 'LenLT')
    
    if overall_sharpe_ratio_3d_scatter:
        plot_overall_sharpe_ratio_3d_scatter(raw_adjusted_returns_df, scatter_params)
