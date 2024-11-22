from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import re

def generate_log_ticks(equity_curve: pd.DataFrame, start_amount: int, num_ticks: int = 6):

    y_min, y_max = equity_curve.min().min(), equity_curve.max().max()
    tick_vals = np.logspace(np.log10(y_min), np.log10(y_max), num=num_ticks)
    tick_vals = np.insert(tick_vals, 0, start_amount)
    tick_vals = np.unique(tick_vals)
    tick_text = [f"{val:.0f}" for val in tick_vals]
    return tick_vals, tick_text

def get_custom_colormap(n_colors: int) -> LinearSegmentedColormap:

    base_colors = ["red", "yellow", "lime", "cyan"]
    cmap_name = "custom_colormap"
    if n_colors == 1:
        # Assurer que la colormap a une seule couleur mais toujours valider pour l'intervalle [0, 1]
        return LinearSegmentedColormap.from_list(cmap_name, [base_colors[0], base_colors[0]], N=2)
    elif n_colors <= len(base_colors):
        # Utilisation des couleurs de base si le nombre de couleurs requis est inférieur ou égal au nombre de couleurs de base
        return LinearSegmentedColormap.from_list(cmap_name, base_colors[:n_colors], N=n_colors)
    else:
        # Génération d'un colormap interpolé si plus de couleurs sont nécessaires
        return LinearSegmentedColormap.from_list(cmap_name, base_colors, N=n_colors)

def get_color(i: int, total: int) -> str:

    cmap = get_custom_colormap(total)
    return cmap(i / total)

def convert_to_surface_grid(x_vals, y_vals, z_vals):

    # Convertir les listes en arrays numpy
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z_vals = np.array(z_vals)

    # Créer une grille régulière à partir des valeurs uniques de x_vals (X) et y_vals (Y)
    x_unique = np.unique(x_vals)
    y_unique = np.unique(y_vals)
    X, Y = np.meshgrid(x_unique, y_unique)

    # Créer une grille Z qui correspond à la surface des Sharpe ratios
    Z = np.full_like(X, np.nan, dtype=np.float32)

    # Remplir la grille Z avec les valeurs correspondantes des Sharpe ratios
    for i in range(len(x_vals)):
        x_idx = np.where(x_unique == x_vals[i])[0][0]
        y_idx = np.where(y_unique == y_vals[i])[0][0]
        Z[y_idx, x_idx] = z_vals[i]

    return X, Y, Z

def extract_params_from_name(name: str, param1: str, param2: str) -> tuple:

    # Create regex patterns for each parameter
    pattern1 = re.compile(f"{param1}(\\d+)")
    pattern2 = re.compile(f"{param2}(\\d+)")
    
    # Search for the parameters in the name
    match1 = pattern1.search(name)
    match2 = pattern2.search(name)
    
    # Extract the values if matches are found, otherwise return None
    param1_value = int(match1.group(1)) if match1 else None
    param2_value = int(match2.group(1)) if match2 else None
    
    return param1_value, param2_value

def extract_all_params_from_name(name: str, params: list) -> list:

    extracted_values = []
    for param in params:
        pattern = re.compile(f"{param}(\\d+)")
        match = pattern.search(name)
        extracted_values.append(int(match.group(1)) if match else None)
    
    return extracted_values