from tradeframe.categorical import FrameCategoricalHorizontal, FrameCategoricalVertical
from tradeframe.implementations import FrameVertical, FrameHorizontal

__all__: list[str] = [
    "FrameCategoricalHorizontal",
    "FrameCategoricalVertical",
    "FrameVertical",
    "FrameHorizontal"
]

# TODO: FAIRE PIPELINE POUR LES 2 VERSIONS POSSIBLES:
# ! METTRE EN PLACE BACKTEST arrays avec format Vertical
# TODO: CHECK LES GRAPHS
# NamedHorizontal: (une col par asset, une ligne par date, les noms d'asset sont les noms de colonnes)
# NamedVertical: (une col par date, une ligne par asset, + 1 col pour les noms d'asset)
# pour chaque version, mettre en place le categorical correspondant

# puis mettre en place long format (une col par attribut(return, date, nom), comme SQL ->
# array, categorical
# il faudra voir comment connecter le datedData

# au final, j'aurai un array filling, un base frame, et un categorical frame de chaque type:
# - vertical, horizontal, long