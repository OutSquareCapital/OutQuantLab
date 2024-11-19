import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import Dashboard.Common as Common
import Dashboard.Widgets as Widgets 
import Dashboard.Computations as Computations
from Portfolio import Static_Clusters
import Metrics as mt

@staticmethod
def equity(equity_curve: pd.DataFrame):
    """
    Plot equity curves.

    Args:
        equity_curve (pd.DataFrame): DataFrame containing equity curves.
        log_scale (bool): Whether to use log scale for the y-axis.
    """
    title = 'Equity Curves'
    xlabel = 'Date'
    ylabel = 'Equity'

    final_values = equity_curve.iloc[-1]
    sorted_columns = final_values.sort_values(ascending=True).index
    n_strats = len(sorted_columns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        y = equity_curve[column]
        Widgets.curves(fig, equity_curve.index, y, label=column, color=color)

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

@staticmethod
def plot_final_equity_values(daily_returns: pd.DataFrame):
    """
    Plot the final equity value if the backtest started each day.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
        initial_equity (int): Initial equity value.
    """
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
    n_strats = len(sorted_columns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

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

        
@staticmethod
def drawdowns(equity_curves: pd.DataFrame):
    """
    Plot drawdowns for each equity curve.

    Args:
        equity_curves (pd.DataFrame): DataFrame containing equity curves.
    """
    drawdowns = Computations.drawdowns_calculs(equity_curves)

    title = "Drawdowns"
    xlabel = "Date"
    ylabel = "Drawdown (%)"

    # Calculating means of drawdowns
    drawdown_means = drawdowns.mean()
    drawdown_percentiles = drawdown_means.rank(pct=True)
    sorted_columns = drawdown_percentiles.sort_values(ascending=True).index
    n_strats = len(sorted_columns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                                        equity_curves.index, 
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

@staticmethod
def max_drawdowns(equity_curves: pd.DataFrame):
    """
    Plot max drawdowns histogram.

    Args:
        equity_curves (pd.DataFrame): DataFrame containing equity curves.
    """
    # Calcul des drawdowns
    drawdowns = Computations.drawdowns_calculs(equity_curves)

    # Calcul des drawdowns maximaux pour chaque stratégie
    max_drawdowns = drawdowns.min(axis=0)

    title = 'Max Drawdowns'
    xlabel = 'Strats'
    ylabel = 'Max Drawdown (%)'

    # Tri des stratégies par drawdown maximal (du plus grand au plus petit drawdown)
    sorted_max_drawdowns = max_drawdowns.sort_values(ascending=True)
    n_strats = len(sorted_max_drawdowns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

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


@staticmethod
def annual_returns(daily_returns: pd.DataFrame):
    """
    Trace les rendements annuels pour chaque courbe d'équité sous forme de tableau.

    Args:
        daily_returns (pd.DataFrame): DataFrame contenant les rendements quotidiens.
    """
    annual_returns = Computations.annual_returns_calculs(daily_returns)

    title = 'Yearly Returns'
    Widgets.colored_table(annual_returns, 
                                            title, 
                                            sort_ascending=True, 
                                            color_high_to_low=False)

@staticmethod
def correlation_heatmap(daily_returns: pd.DataFrame):
    """
    Plot correlation heatmap of equity curve returns.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
    """
    correlation_matrix = daily_returns.corr()

    title = 'Correlation Matrix'
    # Utiliser les labels complets sans simplification
    labels = daily_returns.columns

    plt.figure(figsize=(16, 14))
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=.05,
        xticklabels=labels, 
        yticklabels=labels
    )
    plt.title(title)
    plt.show()
    return correlation_matrix.round(2)


@staticmethod
def average_correlation_bar_chart(daily_returns: pd.DataFrame):
    """
    Plot average correlations of equity curve returns.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
    """
    average_correlations_df = Computations.average_correlation_calculs(daily_returns)

    title = 'Average Correlations'
    xlabel = 'Strats'
    ylabel = 'Average Correlation'

    sorted_correlations = average_correlations_df.sort_values(by='Average Correlation', ascending=False)
    n_strats = len(sorted_correlations)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]
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


@staticmethod
def overall_sharpe_ratios(daily_returns: pd.DataFrame):
    """
    Plot Sharpe ratios histogram.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
    """
    sharpe_ratios_df = Computations.overall_sharpe_ratios_calculs(daily_returns)
    
    title = 'Sharpe Ratios'
    xlabel = 'Strats'
    ylabel = 'Sharpe Ratio'

        # Sort by Sharpe Ratio values
    sorted_sharpe_ratios = sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=True)
    n_strats = len(sorted_sharpe_ratios)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]
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
    return sorted_sharpe_ratios

@staticmethod
def overall_monthly_skew(daily_returns: pd.DataFrame):
    """
    Plot Skew histogram for each asset.
    """
    title = 'Monthly Skew'
    xlabel = 'Strats'
    ylabel = 'Skew'

    skew_series = Computations.overall_monthly_skew_calculs(daily_returns)
    
    # Trier les skew pour un affichage ordonné
    sorted_skew_series = skew_series.sort_values(ascending=True)
    n_strats = len(sorted_skew_series)
    
    # Obtenir un colormap personnalisé pour les barres
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]
    
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
    
@staticmethod
def rolling_sharpe_ratio(daily_returns: pd.DataFrame, window_size: int):
    """
    Plot rolling Sharpe ratios for each equity curve.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
        window_size (int): Window size for rolling calculation.
    """
    rolling_sharpe_ratios = mt.rolling_sharpe_ratios_df(daily_returns, window_size)

    title = f'Rolling Sharpe Ratios Over {window_size} Days'
    xlabel = 'Date'
    ylabel = 'Rolling Sharpe Ratio'
    
    mean_sharpes = {column: np.nanmean(sharpe) for column, sharpe in rolling_sharpe_ratios.items()}
    sorted_columns = sorted(mean_sharpes, key=mean_sharpes.get, reverse=False)
    n_strats = len(sorted_columns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]
    fig = go.Figure()
    for index, column in enumerate(sorted_columns):
        color = colors[index]
        Widgets.curves(fig, 
                                        daily_returns.index,
                                        rolling_sharpe_ratios[column], 
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


@staticmethod
def sharpe_ratios_yearly_table(daily_returns: pd.DataFrame):
    """
    Plot Sharpe ratios for each years.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
    """
    sharpe_ratios_df = Computations.sharpe_ratios_yearly_calculs(daily_returns)

    title = 'Sharpe Ratios per year'
    
    Widgets.colored_table(sharpe_ratios_df, 
                                            title, 
                                            sort_ascending=True, 
                                            color_high_to_low=False)


@staticmethod
def sortino_ratios(daily_returns: pd.DataFrame):

    sortino_ratios_df = Computations.overall_sortino_ratios_calculs(daily_returns)

    title = 'Sortino Ratios'
    xlabel = 'Strats'
    ylabel = 'Sortino Ratio'

    sorted_sortino_ratios = sortino_ratios_df.sort_values(by='Sortino Ratio', ascending=True)
    n_strats = len(sorted_sortino_ratios)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]
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

@staticmethod
def returns_distribution(daily_returns: pd.DataFrame, freq: str = 'H'):
    """
    Plot return distribution of returns.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
        freq (str): Frequency for resampling returns.
    """
    daily_returns = daily_returns * 100
    title = 'Histogram of Strategy % Returns Distribution'
    xlabel = 'Strategy % Returns'
    ylabel = 'Frequency'
    Widgets.histogram(daily_returns, title, xlabel, ylabel)

@staticmethod
def plot_strategy_returns_by_decile(strategy_returns_by_decile: pd.DataFrame):
    """
    Plot strategy returns by volatility decile using Plotly.

    Args:
        strategy_returns_by_decile (pd.DataFrame): DataFrame of strategy returns by volatility decile.
    """
    fig = px.bar(strategy_returns_by_decile, 
                x=strategy_returns_by_decile.index, 
                y=strategy_returns_by_decile.columns, 
                title="Strategy Returns by Volatility Decile", 
                labels={"index": "Volatility Decile", "value": "Strategy Returns"},
                barmode='group')
    fig.update_layout(xaxis_title="Volatility Decile", yaxis_title="Average Strategy Return")
    fig.show()


@staticmethod
def volatility(daily_returns: pd.DataFrame, means=False):

    if means:
        rolling_volatility_df = pd.DataFrame(mt.hv_composite(daily_returns.values), 
                                             index=daily_returns.index, 
                                             columns=daily_returns.columns)
        rolling_volatility_df = rolling_volatility_df.expanding(min_periods=1).mean()
    else:
        rolling_volatility_df = pd.DataFrame(mt.hv_composite(daily_returns.values), 
                                             index=daily_returns.index, 
                                             columns=daily_returns.columns)

    rolling_volatility_df = rolling_volatility_df.round(2)
    
    title = f'Rolling Volatility'
    xlabel = 'Date'
    ylabel = 'Rolling Volatility (%)'

    rolling_volatility_means = rolling_volatility_df.mean()
    rolling_volatility_percentiles = rolling_volatility_means.rank(pct=True)
    sorted_columns = rolling_volatility_percentiles.sort_values(ascending=True).index
    n_strats = len(sorted_columns)
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

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
    return rolling_volatility_means.sort_values(ascending=True)


@staticmethod
def sharpe_ratios_3d_surface_plot(daily_returns: pd.DataFrame, param1: str, param2: str):
    """
    Generate a 3D surface plot with two parameters on the X and Y axes, and the Sharpe ratio on the Z axis,
    while colorizing the surface based on the Sharpe/AvgCorrelation metric.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns for different strategies.
        param1 (str): The first parameter to plot on the X axis.
        param2 (str): The second parameter to plot on the Y axis.
    """
    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = mt.overall_sharpe_ratios_calculs(daily_returns)
    
    # Calcul de la nouvelle métrique via la fonction calculate_sharpe_correlation_ratio
    combined_df = Computations.calculate_sharpe_correlation_ratio(daily_returns)

    # Initialiser des dictionnaires pour stocker les Sharpe ratios et la nouvelle métrique Sharpe/AvgCorrelation par (param1, param2)
    sharpe_dict = defaultdict(list)
    sharpe_corr_dict = defaultdict(list)

    # Extraire les paramètres et les ratios de Sharpe ainsi que la nouvelle métrique Sharpe/AvgCorrelation
    for index, row in sharpe_ratios_df.iterrows():
        param1_value, param2_value = Computations.extract_params_from_name(index, param1, param2)

        if param1_value is not None and param2_value is not None:
            # Stocker le Sharpe Ratio
            sharpe_dict[(param1_value, param2_value)].append(row['Sharpe Ratio'])
            # Stocker la nouvelle métrique Sharpe/AvgCorrelation
            sharpe_corr_dict[(param1_value, param2_value)].append(combined_df.loc[index, 'Sharpe/AvgCorrelation'])

    # Initialiser les listes pour les valeurs moyennes des Sharpe ratios et Sharpe/AvgCorrelation
    x_vals = []
    y_vals = []
    z_vals = []
    color_vals = []

    # Calculer les moyennes des Sharpe ratios et de la nouvelle métrique pour chaque combinaison (param1, param2)
    for (p1, p2), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(np.nanmean(sharpe_list))  # Moyenne des Sharpe ratios
        color_vals.append(np.nanmean(sharpe_corr_dict[(p1, p2)]))  # Moyenne de Sharpe/AvgCorrelation

    # Utiliser la fonction pour convertir les données en surface
    X, Y, Z = Common.convert_to_surface_grid(x_vals, y_vals, z_vals)
    _, _, color_surface = Common.convert_to_surface_grid(x_vals, y_vals, color_vals)

    # Créer une surface 3D avec Plotly, où la couleur est basée sur Sharpe/AvgCorrelation
    fig = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,
        surfacecolor=color_surface,  # Utilisation de Sharpe/AvgCorrelation pour coloriser
        colorscale='Jet_r',
        showscale=True,
        colorbar=dict(title='Sharpe/AvgCorrelation'),
        hovertemplate='Param1: %{x}<br>Param2: %{y}<br>Sharpe Ratio: %{z:.2f}<br>Sharpe/AvgCorrelation: %{surfacecolor:.2f}<extra></extra>'
    )])

    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        title=f'3D Sharpe Ratios Surface with Color Based on Sharpe/AvgCorrelation for {param1} and {param2}',
        scene=dict(
            xaxis_title=param1,
            yaxis_title=param2,
            zaxis_title='Sharpe Ratio'
        ),
        template="plotly_dark",
        height=800
    )

    # Afficher le graphique
    fig.show()

@staticmethod
def sharpe_correlation_3d_surface_plot(daily_returns: pd.DataFrame, param1: str, param2: str):
    """
    Generate a 3D surface plot with two parameters on the X and Y axes, and the Sharpe/AvgCorrelation on the Z axis,
    while colorizing the surface based on the Sharpe ratio.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns for different strategies.
        param1 (str): The first parameter to plot on the X axis.
        param2 (str): The second parameter to plot on the Y axis.
    """
    # Calcul de la nouvelle métrique via la fonction calculate_sharpe_correlation_ratio
    combined_df = Computations.calculate_sharpe_correlation_ratio(daily_returns)
    
    # Calcul des Sharpe Ratios pour chaque stratégie
    sharpe_ratios_df = mt.overall_sharpe_ratios_calculs(daily_returns)

    # Initialiser des dictionnaires pour stocker la nouvelle métrique Sharpe/AvgCorrelation et les Sharpe Ratios par (param1, param2)
    sharpe_corr_dict = defaultdict(list)
    sharpe_dict = defaultdict(list)

    # Extraire les paramètres et les valeurs des deux métriques
    for index, row in sharpe_ratios_df.iterrows():
        param1_value, param2_value = Computations.extract_params_from_name(index, param1, param2)

        if param1_value is not None and param2_value is not None:
            # Stocker le Sharpe/AvgCorrelation
            sharpe_corr_dict[(param1_value, param2_value)].append(combined_df.loc[index, 'Sharpe/AvgCorrelation'])
            # Stocker le Sharpe Ratio
            sharpe_dict[(param1_value, param2_value)].append(row['Sharpe Ratio'])

    # Initialiser les listes pour les valeurs moyennes des Sharpe/AvgCorrelation (Z) et Sharpe Ratios (coloration)
    x_vals = []
    y_vals = []
    z_vals = []
    color_vals = []

    # Calculer les moyennes pour chaque combinaison (param1, param2)
    for (p1, p2), sharpe_corr_list in sharpe_corr_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(np.nanmean(sharpe_corr_list))  # Moyenne de Sharpe/AvgCorrelation (pour l'axe Z)
        color_vals.append(np.nanmean(sharpe_dict[(p1, p2)]))  # Moyenne du Sharpe Ratio (pour la couleur)

    # Utiliser la fonction pour convertir les données en surface
    X, Y, Z = Common.convert_to_surface_grid(x_vals, y_vals, z_vals)
    _, _, color_surface = Common.convert_to_surface_grid(x_vals, y_vals, color_vals)

    # Créer une surface 3D avec Plotly, où la couleur est basée sur le Sharpe Ratio
    fig = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,  # L'axe Z est maintenant Sharpe/AvgCorrelation
        surfacecolor=color_surface,  # Couleur basée sur Sharpe Ratio
        colorscale='Jet_r',
        showscale=True,
        colorbar=dict(title='Sharpe Ratio'),  # Légende pour la couleur représentant le Sharpe Ratio
        hovertemplate='Param1: %{x}<br>Param2: %{y}<br>Sharpe/AvgCorrelation: %{z:.2f}<br>Sharpe Ratio: %{surfacecolor:.2f}<extra></extra>'
    )])

    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        title=f'3D Surface of Sharpe/AvgCorrelation (Z) with Color Based on Sharpe Ratio for {param1} and {param2}',
        scene=dict(
            xaxis_title=param1,
            yaxis_title=param2,
            zaxis_title='Sharpe/AvgCorrelation'
        ),
        template="plotly_dark",
        height=800
    )

    # Afficher le graphique
    fig.show()



@staticmethod
def sharpe_ratios_3d_scatter_plot(daily_returns: pd.DataFrame, params: list):
    """
    Generate a 3D scatter plot with three parameters and Sharpe Ratio as the color. 
    If more than three parameters are provided, calculate the mean Sharpe ratio for each combination 
    of the first three parameters.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns for different strategies.
        params (list): List of parameter names to extract (e.g., ['param1', 'param2', 'param3']).
    """
    x_vals, y_vals, z_vals, sharpe_means = Computations.calculate_sharpe_means_from_combination(daily_returns, params)

    # Créer un scatter 3D avec les couleurs basées sur la moyenne du Sharpe Ratio
    fig = go.Figure(data=[go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers',
        marker=dict(
            size=8,  # Taille des points
            color=sharpe_means,  # Couleur en fonction du Sharpe Ratio moyen
            colorscale='Jet_r',  # Palette de couleurs pour représenter le Sharpe Ratio
            colorbar=dict(title="Sharpe Ratio"),  # Barre de couleur pour Sharpe Ratio
            showscale=True
        ),
        text=['Sharpe Ratio moyen: {:.2f}'.format(sr) for sr in sharpe_means],  # Info bulle pour chaque point
        hovertemplate='Param1: %{x}<br>Param2: %{y}<br>Param3: %{z}<br>Sharpe Ratio: %{marker.color}<extra></extra>'
    )])

    # Mise à jour de la mise en page du graphique
    fig.update_layout(
        scene=dict(
            xaxis_title=params[0],
            yaxis_title=params[1],
            zaxis_title=params[2]
        ),
        template="plotly_dark",
        title=f'Scatter Plot 3D des Sharpe Ratios pour {params[0]}, {params[1]} et {params[2]}',
        height=800
    )

    # Affichage du graphique
    fig.show()

@staticmethod
def sharpe_ratios_heatmap(daily_returns: pd.DataFrame, param1: str, param2: str):
    """
    Generate a heatmap with two parameters on the X and Y axes, and the Sharpe ratio represented by the color intensity,
    calculating the mean of the Sharpe ratios for strategies with the same param1 and param2 values.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns for different strategies.
        param1 (str): The first parameter to plot on the X axis.
        param2 (str): The second parameter to plot on the Y axis.
    """
    # Calcul du ratio de Sharpe pour chaque stratégie
    sharpe_ratios_df = mt.overall_sharpe_ratios_calculs(daily_returns)

    # Initialiser un dictionnaire pour stocker les Sharpe ratios par (param1, param2)
    sharpe_dict = defaultdict(list)

    # Extraire les paramètres et les ratios de Sharpe à partir de l'index
    for index, row in sharpe_ratios_df.iterrows():
        # Extraire les deux paramètres principaux
        param1_value, param2_value = Computations.extract_params_from_name(index, param1, param2)

        # Si on trouve les deux valeurs de param1 et param2, on stocke le Sharpe ratio
        if param1_value is not None and param2_value is not None:
            sharpe_dict[(param1_value, param2_value)].append(row['Sharpe Ratio'])

    # Initialiser les listes pour les valeurs moyennes des Sharpe ratios
    x_vals = []
    y_vals = []
    z_vals = []

    # Calculer les moyennes des Sharpe ratios pour chaque combinaison (param1, param2)
    for (p1, p2), sharpe_list in sharpe_dict.items():
        x_vals.append(p1)
        y_vals.append(p2)
        z_vals.append(np.nanmean(sharpe_list))  # Moyenne des Sharpe ratios

    # Convertir les listes en un grid de type heatmap
    X, Y, Z = Common.convert_to_surface_grid(x_vals, y_vals, z_vals)

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


@staticmethod
def params_relative_impact_on_sharpe(daily_returns: pd.DataFrame, params: list):
    """
    Perform parameter sensitivity analysis and plot sorted regression coefficients in a bar chart.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns.
        params (list): List of parameter names to analyze (e.g., ['LenST', 'LenLT', 'MacdLength']).
    """
    # Analyse de sensibilité des paramètres (obtenir les coefficients triés)
    sorted_coefficients = Computations.analyze_param_sensitivity(daily_returns, params)

    title = 'Sorted Regression Coefficients'
    xlabel = 'Parameters'
    ylabel = 'Absolute Coefficient Value'

    n_params = len(sorted_coefficients)
    cmap = Common.get_custom_colormap(n_params)
    if n_params == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_params - 1))) for i in range(n_params)]
    
    fig = go.Figure()

    # Ajout des barres pour chaque coefficient trié
    for index, (param, coefficient) in enumerate(sorted_coefficients.items()):
        color = colors[index]
        Widgets.bar(fig, x=[index], y=[coefficient], label=param, color=color)

    # Mise à jour du layout
    fig.update_layout(
        title=title,
        xaxis=dict(
            tickvals=list(range(n_params)),
            ticktext=sorted_coefficients.index
        ),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_dark"
    )

    # Affichage du graphique
    fig.show()


@staticmethod
def sharpe_correlation_ratio_bar_chart(daily_returns: pd.DataFrame):
    """
    Plot a bar chart showing Sharpe Ratio Rank divided by Average Correlation Rank for each strategy.

    Args:
        daily_returns (pd.DataFrame): DataFrame containing daily returns for different strategies.
    """
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

    # Générer une colormap pour les barres
    cmap = Common.get_custom_colormap(n_strats)
    if n_strats == 1:
        colors = ['white']
    else:
        colors = [mcolors.to_hex(cmap(i / (n_strats - 1))) for i in range(n_strats)]

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

@staticmethod
def plot_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters):
    """
    Prépare les données pour le Sunburst/Treemap et affiche le graphique avec Plotly.
    
    Args:
        clusters_dict (dict): La structure des clusters.
    """
    clusters_dict = Static_Clusters.generate_static_clusters(returns_df, max_clusters, max_sub_clusters, max_sub_sub_clusters)

    def prepare_sunburst_data(cluster_dict, parent_label="", labels=None, parents=None):
        """
        Prépare les données pour le Sunburst Plot en formatant les clusters récursivement.
        
        Args:
            cluster_dict (dict): La structure des clusters.
            parent_label (str): Nom du parent actuel dans la hiérarchie.
            labels (list): Liste des noms pour les feuilles.
            parents (list): Liste des parents pour chaque feuille.

        Returns:
            tuple: Deux listes contenant les labels et les parents pour le Sunburst plot.
        """
        if labels is None:
            labels = []  # Réinitialisation de la liste à chaque appel
        if parents is None:
            parents = []  # Réinitialisation de la liste à chaque appel
            
        for key, value in cluster_dict.items():
            current_label = parent_label + str(key) if parent_label else str(key)  # Construit le label courant
            if isinstance(value, dict):
                # Si c'est un sous-cluster, on continue la récursion
                prepare_sunburst_data(value, current_label, labels, parents)
            else:
                # Si on arrive à une liste d'actifs, on les ajoute comme feuilles
                for asset in value:
                    labels.append(asset)
                    parents.append(current_label)
            # Ajouter le cluster actuel comme nœud s'il a des enfants
            if parent_label:
                labels.append(current_label)
                parents.append(parent_label)
            else:
                labels.append(current_label)
                parents.append("")  # Root node has no parent
                
        return labels, parents

    # Préparer les données pour le Sunburst
    labels, parents = prepare_sunburst_data(clusters_dict)

    # Créer le Sunburst/Treemap Plot avec Plotly
    fig = px.treemap(
        names=labels,
        parents=parents,
        title="Visualisation des Clusters",
        maxdepth=-1  # Affiche toute la hiérarchie
    )

    # Afficher la figure
    fig.show()


def nan_param_dict(daily_returns, params):
    """
    Visualise les zones de NaN en fonction de param1, param2 et param3 avec Plotly et retourne un dictionnaire des zones occupées.
    Regroupe et ordonne les combinaisons de param1 et param2 qui apparaissent dans chaque param3.
    
    Args:
    daily_returns (pd.DataFrame): DataFrame contenant les retours journaliers des stratégies.
    params (list): Liste des paramètres à extraire des noms des stratégies.
    
    Returns:
    dict: Un dictionnaire des zones où les NaN apparaissent, regroupées par param3 et param1 communs.
    """
    # Étape 1 : Calculer les moyennes des Sharpe ratios par combinaison de paramètres
    x_vals, y_vals, z_vals, sharpe_means = Computations.calculate_sharpe_means_from_combination(daily_returns, params)
    
    # Étape 2 : Créer un DataFrame pour plus de facilité
    sharpe_df = pd.DataFrame({
        'param1': x_vals,
        'param2': y_vals,
        'param3': z_vals,
        'sharpe': sharpe_means
    })
    
    # Étape 3 : Filtrer les lignes où le Sharpe Ratio est NaN
    nan_df = sharpe_df[sharpe_df['sharpe'].isna()]

    # Étape 4 : Regrouper les combinaisons par param3 et param1 communs
    nan_zones = defaultdict(lambda: defaultdict(list))  # Dictionnaire imbriqué

    for param3 in nan_df['param3'].unique():  # Parcourir chaque param3
        for param1 in nan_df[nan_df['param3'] == param3]['param1'].unique():  # Parcourir chaque param1 pour ce param3
            param2_list = nan_df[(nan_df['param3'] == param3) & (nan_df['param1'] == param1)]['param2'].tolist()
            nan_zones[param3][param1] = sorted(param2_list)  # Trier les param2 pour chaque param1

    # Tri des résultats par param3
    sorted_nan_zones = {}
    for param3 in sorted(nan_zones.keys()):  # Tri des param3
        sorted_nan_zones[param3] = {}
        for param1 in sorted(nan_zones[param3].keys()):  # Tri des param1
            sorted_nan_zones[param3][param1] = sorted(nan_zones[param3][param1])  # Tri des param2

    return sorted_nan_zones