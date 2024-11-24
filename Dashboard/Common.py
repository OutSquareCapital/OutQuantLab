from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors

def generate_colormap(n_colors: int) -> LinearSegmentedColormap:

    base_colors = ["red", "yellow", "lime", "cyan"]
    cmap_name = "custom_colormap"
    if n_colors == 1:
        return LinearSegmentedColormap.from_list(cmap_name, [base_colors[0], base_colors[0]], N=2)
    elif n_colors <= len(base_colors):
        return LinearSegmentedColormap.from_list(cmap_name, base_colors[:n_colors], N=n_colors)
    else:
        return LinearSegmentedColormap.from_list(cmap_name, base_colors, N=n_colors)
    
def map_colors_to_columns(n_colors: int) -> list:

    cmap = generate_colormap(n_colors)
    return [mcolors.to_hex(cmap(i / (n_colors - 1))) for i in range(n_colors)]

def get_color_map(assets: list) -> dict:

    n_colors = len(assets)
    colors = map_colors_to_columns(n_colors)
    return dict(zip(assets, colors))

