import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import numpy as np
import Dashboard.Format as Format

def colored_table(df: pd.DataFrame, title: str, sort_ascending: bool = True, color_high_to_low: bool = True):

    # Arrondir les valeurs à 4
    df = df.round(4)

    avg_performance = df.mean()
    sorted_assets = avg_performance.sort_values(ascending=not color_high_to_low).index
    # Association des couleurs aux actifs triés
    asset_colors = {asset: mcolors.to_hex(Format.get_color(i, len(sorted_assets))) for i, asset in enumerate(sorted_assets)}

    sorted_values = []
    sorted_colors = []
    for idx, row in df.iterrows():
        na_values = row.isna()  # Identification des valeurs manquantes
        # Tri des valeurs non manquantes
        non_na_values = row.dropna().sort_values(ascending=sort_ascending)
        # Concaténation des valeurs manquantes et non manquantes
        sorted_row = np.concatenate([row[na_values].values, non_na_values.values])
        sorted_values.append(sorted_row)

        # Création d'une liste de couleurs correspondant aux valeurs
        row_colors = ['black'] * na_values.sum() + [asset_colors[col] for col in non_na_values.index]
        sorted_colors.append(row_colors)

    sorted_values_df = pd.DataFrame(sorted_values, index=df.index, dtype=np.float32)
    sorted_colors = np.array(sorted_colors).T.tolist()  # Transposition pour correspondre à la structure des cellules
    text_colors = [['black'] * len(row) for row in sorted_values]  # Couleurs du texte pour chaque cellule

    fig = go.Figure(data=[go.Table(
        header=dict(values=['Year'] + [''] * (sorted_values_df.shape[1] - 1),
                    fill_color='black',
                    font=dict(color='white'),
                    align='center'),
        cells=dict(values=[sorted_values_df.index.astype(str).tolist()] + [sorted_values_df[col].tolist() for col in sorted_values_df.columns],
                fill_color=[['black'] * len(sorted_values_df)] + sorted_colors,
                align='center',
                font=dict(color=[['white']] + text_colors))
    )])
    # Ajout des annotations pour la légende des couleurs
    annotations = [
        dict(x=1.25, y=1.05 - (i * 0.05), xref='paper', yref='paper',
            text=f'<span style="color:{asset_colors[asset]}">{asset}</span>',
            showarrow=False, align='left') for i, asset in enumerate(sorted_assets)
    ]

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        plot_bgcolor='#2b2b2b',
        paper_bgcolor='#2b2b2b',
        font=dict(color='white'),
        height=800,
        width=1000,
        margin=dict(r=200,
        ),
        annotations=annotations
    )
    fig.show()
    plt.close()

def bar(fig: go.Figure, x: list, y: list, label: str, color: str, show_x_axis: bool = False):

    fig.add_trace(go.Bar(
        x=x,
        y=y,
        name=label,
        marker_color=color
    ))
    if not show_x_axis:
        fig.update_layout(xaxis=dict(showticklabels=False))
    plt.close()


def curves(fig: go.Figure, x: list, y: list, label: str, color: str, add_zero_line: bool = False):

    if len(y) == 0:
        return
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=label,
        line=dict(width=2, color=color),
        showlegend=True
    ))
    if add_zero_line:
        fig.add_trace(go.Scatter(
            x=x,
            y=[0] * len(x),
            mode='lines',
            name='Zero Line',
            line=dict(width=2, color='white'),
            showlegend=False
        ))

def histogram(df: pd.DataFrame, title: str, xlabel: str, ylabel: str):

    df = df*100
    # Flatten the DataFrame for Plotly
    melted_data = df.melt(var_name='Strat', value_name='Returns')

    # Create a color map for the assets
    unique_assets = melted_data['Strat'].unique()
    colors = [Format.get_color(i, len(unique_assets)) for i in range(len(unique_assets))]
    color_map = dict(zip(unique_assets, colors))

    # Plot using Plotly Express
    fig = px.histogram(
        melted_data,
        x='Returns',
        color='Strat',
        nbins=50,
        title=title,
        labels={'Returns': xlabel},
        opacity=0.5,
        barmode='overlay',
        color_discrete_map={k: mcolors.to_hex(v) for k, v in color_map.items()}
    )
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template='plotly_dark',
        yaxis_type='log'  # Ajout de l'axe y en échelle logarithmique
    )
    fig.show()
    plt.close()