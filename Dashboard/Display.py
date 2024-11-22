import matplotlib.colors as mcolors
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
    n_strats = len(sorted_columns)
    colors = Common.map_colors_to_columns(n_strats, sorted_columns)

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        y = equity_curves[column]
        Widgets.curves(fig, equity_curves.index, y, label=column, color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(
            type="log" ,
            tickmode='array'
        ),
        template="plotly_dark",
        height=800
    )
    fig.show()


def plot_final_equity_values(daily_returns: pd.DataFrame):

    # Calcul des valeurs finales de l'équity
    final_equities_df = Computations.calculate_final_equity_values(daily_returns)

    title = 'Final Equity Value Starting Each Day'
    xlabel = 'Start Date'
    ylabel = 'Final Equity Value'

    # Calculating means of final equities
    final_equity_means = final_equities_df.mean()
    final_equity_percentiles = final_equity_means.rank(pct=True)
    sorted_columns = final_equity_percentiles.sort_values(ascending=True).index

    fig = go.Figure()

    colors = Common.map_colors_to_columns(len(sorted_columns), sorted_columns)


    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                        final_equities_df.index, 
                        final_equities_df[column], 
                        label=column, 
                        color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        yaxis=dict(
            type="log" ,
            tickmode='array'
        ),
        template="plotly_dark"
    )
    fig.show()

        

def drawdowns(returns_df: pd.DataFrame):

    drawdowns = Computations.drawdowns_calculs(returns_df)

    title = "Drawdowns"
    xlabel = "Date"
    ylabel = "Drawdown (%)"

    # Calculating means of drawdowns
    drawdown_means = drawdowns.mean()
    drawdown_percentiles = drawdown_means.rank(pct=True)
    sorted_columns = drawdown_percentiles.sort_values(ascending=True).index

    colors = Common.map_colors_to_columns(len(sorted_columns), sorted_columns)

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                                        returns_df.index, 
                                        drawdowns[column], 
                                        label=column.replace('Equity_', '').replace('_Drawdown', ''), 
                                        color=color,
                                        add_zero_line=True)
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()


def max_drawdowns(equity_curves: pd.DataFrame):

    # Calcul des drawdowns
    drawdowns = Computations.drawdowns_calculs(equity_curves)

    # Calcul des drawdowns maximaux pour chaque stratégie
    max_drawdowns = drawdowns.min(axis=0)

    title = 'Max Drawdowns'
    xlabel = 'Strats'
    ylabel = 'Max Drawdown (%)'

    # Tri des stratégies par drawdown maximal (du plus grand au plus petit drawdown)
    sorted_max_drawdowns = max_drawdowns.sort_values(ascending=True)
    colors = Common.map_colors_to_columns(len(sorted_max_drawdowns), sorted_max_drawdowns.index)

    fig = go.Figure()
    for index, column in enumerate(sorted_max_drawdowns.index):
        color = colors[index]
        max_drawdown = sorted_max_drawdowns[column]
        Widgets.bar(fig, x=[index], y=[max_drawdown], label=column, color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()

def annual_returns(daily_returns: pd.DataFrame):

    annual_returns = Computations.annual_returns_calculs(daily_returns)

    title = 'Yearly Returns'
    Widgets.colored_table(annual_returns, 
                            title, 
                            sort_ascending=True, 
                            color_high_to_low=False)

def correlation_heatmap(daily_returns: pd.DataFrame):
    correlation_matrix = daily_returns.corr()
    Widgets.heatmap(correlation_matrix, daily_returns.columns, "Correlation Matrix")

def average_correlation_bar_chart(daily_returns: pd.DataFrame):

    average_correlations_df = Computations.average_correlation_calculs(daily_returns)

    title = 'Average Correlations'
    xlabel = 'Strats'
    ylabel = 'Average Correlation'

    sorted_correlations = average_correlations_df.sort_values(by='Average Correlation', ascending=False)
    n_strats = len(sorted_correlations)
    colors = Common.map_colors_to_columns(n_strats, sorted_correlations.index)

    fig = go.Figure()
    for index, (column, row) in enumerate(sorted_correlations.iterrows()):
        color = colors[index]
        mean_corr = row['Average Correlation']
        Widgets.bar(fig, x=[index], y=[mean_corr], label=column, color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()



def overall_sharpe_ratios(daily_returns: pd.DataFrame):

    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)
    
    title = 'Sharpe Ratios'
    xlabel = 'Strats'
    ylabel = 'Sharpe Ratio'

    # Sort by Sharpe Ratio values
    sorted_sharpe_ratios = sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=True)

    colors = Common.map_colors_to_columns(len(sorted_sharpe_ratios), sorted_sharpe_ratios)

    fig = go.Figure()
    for index, (column, row) in enumerate(sorted_sharpe_ratios.iterrows()):
        color = colors[index]
        sharpe_ratio = row['Sharpe Ratio']
        Widgets.bar(fig, x=[index], y=[sharpe_ratio], label=column, color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()


def overall_monthly_skew(daily_returns: pd.DataFrame):

    title = 'Monthly Skew'
    xlabel = 'Strats'
    ylabel = 'Skew'

    skew_series = Computations.overall_monthly_skew_calculs(daily_returns)
    
    # Trier les skew pour un affichage ordonné
    sorted_skew_series = skew_series.sort_values(ascending=True)
    n_strats = len(sorted_skew_series)
    
    colors = Common.map_colors_to_columns(n_strats, sorted_skew_series.index)

    # Création de la figure
    fig = go.Figure()
    for index, (column, skew_value) in enumerate(sorted_skew_series.items()):
        color = colors[index]
        Widgets.bar(fig, x=[index], y=[skew_value], label=column, color=color)
    
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()
    

def rolling_sharpe_ratio(daily_returns: pd.DataFrame):

    rolling_sharpe_ratio_df = Computations.rolling_sharpe_ratios_calculs(daily_returns)
    title = f'Rolling Sharpe Ratios'
    xlabel = 'Date'
    ylabel = 'Rolling Sharpe Ratio'
    
    mean_sharpes = {column: np.nanmean(sharpe) for column, sharpe in rolling_sharpe_ratio_df.items()}
    sorted_columns = sorted(mean_sharpes, key=mean_sharpes.get, reverse=False)

    colors = Common.map_colors_to_columns(len(sorted_columns), sorted_columns)

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                                        daily_returns.index,
                                        rolling_sharpe_ratio_df[column], 
                                        label=column, 
                                        color=color,
                                        add_zero_line=True)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark",
        height=800
    )

    fig.show()

def sharpe_ratios_yearly_table(daily_returns: pd.DataFrame):

    sharpe_ratios_df = Computations.sharpe_ratios_yearly_calculs(daily_returns)

    title = 'Sharpe Ratios per year'
    
    Widgets.colored_table(sharpe_ratios_df, 
                            title, 
                            sort_ascending=True, 
                            color_high_to_low=False)

def sortino_ratios(daily_returns: pd.DataFrame):

    sortino_ratios_df = Computations.overall_sortino_ratios_calculs(daily_returns)

    title = 'Sortino Ratios'
    xlabel = 'Strats'
    ylabel = 'Sortino Ratio'

    sorted_sortino_ratios = sortino_ratios_df.sort_values(by='Sortino Ratio', ascending=True)
    n_strats = len(sorted_sortino_ratios)
    colors = Common.map_colors_to_columns(n_strats, sorted_sortino_ratios.index)
    fig = go.Figure()
    for index, (column, row) in enumerate(sorted_sortino_ratios.iterrows()):
        color = colors[index]
        sortino_ratio = row['Sortino Ratio']
        label = column.replace('Equity_', '').replace('_All_Periods', '')
        Widgets.bar(fig, x=[index], y=[sortino_ratio], label=label, color=color)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )
    fig.show()


def returns_distribution(daily_returns: pd.DataFrame, freq: str = 'H'):

    title = 'Histogram of Strategy % Returns Distribution'
    xlabel = 'Strategy % Returns'
    ylabel = 'Frequency'
    Widgets.histogram(daily_returns, title, xlabel, ylabel)


def volatility(daily_returns: pd.DataFrame, means=False):
    
    rolling_volatility_df = Computations.rolling_volatility_calculs(daily_returns, means)

    title = f'Rolling Volatility'
    xlabel = 'Date'
    ylabel = 'Rolling Volatility (%)'

    rolling_volatility_means = rolling_volatility_df.mean()
    rolling_volatility_percentiles = rolling_volatility_means.rank(pct=True)
    sorted_columns = rolling_volatility_percentiles.sort_values(ascending=True).index
    n_strats = len(sorted_columns)

    colors = Common.map_colors_to_columns(n_strats, sorted_columns)

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                        daily_returns.index, 
                        rolling_volatility_df[column],
                        label=column, 
                        color=color, 
                        add_zero_line=True)

    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )

    fig.show()

def sharpe_ratios_3d_scatter_plot(daily_returns: pd.DataFrame, params: list):

    x_vals, y_vals, z_vals, sharpe_means = Transformations.convert_params_to_4d(daily_returns, params)
    Widgets.scatter_3d(x_vals, y_vals, z_vals, sharpe_means, params, "Scatter Plot 3D")

def sharpe_ratios_heatmap(daily_returns: pd.DataFrame, param1: str, param2: str):

    # Convertir les listes en un grid de type heatmap
    X, Y, Z = Transformations.convert_params_to_3d(daily_returns, param1, param2)

    # Créer une heatmap avec Plotly
    fig = go.Figure(data=go.Heatmap(
        z=Z,
        x=X[0],  # Les valeurs X doivent être prises directement de la grille
        y=Y[:, 0],  # Les valeurs Y doivent être prises directement de la grille
        colorscale='Jet_r',
        colorbar=dict(title='Sharpe Ratio'),
        hovertemplate='Param1: %{x}<br>Param2: %{y}<br>Sharpe Ratio: %{z}<extra></extra>'
    ))

    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        title=f'Heatmap of Sharpe Ratios for {param1} and {param2}',
        xaxis_title=param1,
        yaxis_title=param2,
        template="plotly_dark",
        height=800
    )

    # Affichage du graphique
    fig.show()

def sharpe_correlation_ratio_bar_chart(daily_returns: pd.DataFrame):

    # Calculer la nouvelle métrique via la fonction séparée
    combined_df = Computations.calculate_sharpe_correlation_ratio(daily_returns)

    # Trier par la nouvelle métrique
    sorted_combined_df = combined_df.sort_values(by='Sharpe/AvgCorrelation', ascending=True)

    # Titre et labels
    title = 'Sharpe Ratio Rank / Average Correlation Rank'
    xlabel = 'Strats'
    ylabel = 'Sharpe / Avg Correlation'

    # Nombre de stratégies
    n_strats = len(sorted_combined_df)

    colors = Common.map_colors_to_columns(n_strats, sorted_combined_df.index)

    # Créer la figure avec Plotly
    fig = go.Figure()

    # Ajouter les barres pour chaque stratégie
    for index, (strategy, row) in enumerate(sorted_combined_df.iterrows()):
        sharpe_corr_ratio = row['Sharpe/AvgCorrelation']
        color = colors[index]
        
        # Ajouter une barre pour chaque stratégie
        Widgets.bar(fig, x=[index], y=[sharpe_corr_ratio], label=strategy, color=color)

    # Mettre à jour la mise en page du graphique
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )

    # Afficher le graphique
    fig.show()


def plot_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):

    clusters_dict = generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)
    labels, parents = Transformations.prepare_sunburst_data(clusters_dict)
    Widgets.treemap(labels, parents, "Visualisation des Clusters")
