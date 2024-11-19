from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import re

@staticmethod
def generate_log_ticks(equity_curve: pd.DataFrame, start_amount: int, num_ticks: int = 6):
    """
    Generate logarithmic tick values for y-axis.

    Args:
        equity_curve (pd.DataFrame): DataFrame containing equity curves.
        start_amount (int): Starting amount for all equity curves.
        num_ticks (int): Number of tick values to generate.

    Returns:
        tick_vals (np.ndarray): Array of tick values.
        tick_text (list): List of tick text labels.
    """
    y_min, y_max = equity_curve.min().min(), equity_curve.max().max()
    tick_vals = np.logspace(np.log10(y_min), np.log10(y_max), num=num_ticks)
    tick_vals = np.insert(tick_vals, 0, start_amount)
    tick_vals = np.unique(tick_vals)
    tick_text = [f"{val:.0f}" for val in tick_vals]
    return tick_vals, tick_text


@staticmethod
def get_custom_colormap(n_colors: int) -> LinearSegmentedColormap:
    """
    Get a custom colormap with the specified number of colors.

    Args:
        n_colors (int): Number of colors required.

    Returns:
        LinearSegmentedColormap: Generated colormap.
    """
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


@staticmethod
def get_color(i: int, total: int) -> str:
    """
    Get a specific color from the custom colormap based on the index and total number of colors.

    Args:
        i (int): Index of the color.
        total (int): Total number of colors.

    Returns:
        str: Hex color code.
    """
    cmap = get_custom_colormap(total)
    return cmap(i / total)


@staticmethod
def convert_to_surface_grid(x_vals, y_vals, z_vals):
    """
    Convert lists of x, y, and z values into a regular grid for surface plotting.

    Args:
        x_vals (list): List of x-values (first parameter, e.g., ZScoreLength).
        y_vals (list): List of y-values (second parameter, e.g., PercentileLength).
        z_vals (list): List of z-values (Sharpe ratios or another metric).

    Returns:
        tuple: Three 2D numpy arrays (X, Y, Z) that represent the grid for surface plotting.
    """
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

@staticmethod
def extract_params_from_name(name: str, param1: str, param2: str) -> tuple:
    """
    Extract specific parameters from the strategy name using regex.

    Args:
        name (str): The strategy name formatted as 'asset_strategyclass_strategymethod_strategyparameter'.
        param1 (str): The first parameter to extract (e.g., 'ZScoreLength').
        param2 (str): The second parameter to extract (e.g., 'PercentileLength').

    Returns:
        tuple: A tuple containing the values of the two parameters as integers (param1_value, param2_value).
    """
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


@staticmethod
def extract_all_params_from_name(name: str, params: list) -> list:
    """
    Extract specific parameters from the strategy name using regex, based on a list of parameters.

    Args:
        name (str): The strategy name formatted as 'asset_strategyclass_strategymethod_strategyparameter'.
        params (list): A list of parameters to extract (e.g., ['ZScoreLength', 'PercentileLength']).

    Returns:
        list: A list containing the values of the parameters in the same order as the input list. None if not found.
    """
    extracted_values = []
    for param in params:
        pattern = re.compile(f"{param}(\\d+)")
        match = pattern.search(name)
        extracted_values.append(int(match.group(1)) if match else None)
    
    return extracted_values