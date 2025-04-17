from tradeframe.categorical import FrameCategorical, FrameCategoricalLong
from tradeframe.interfaces import FrameDefault, FrameDefaultHorizontal

__all__: list[str] = [
    "FrameCategorical",
    "FrameCategoricalLong",
    "FrameDefault",
    "FrameDefaultHorizontal"
]

# TODO: FAIRE PIPELINE POUR LES 2 VERSIONS POSSIBLES:
# ! RENAME les classes
# ! METTRE EN PLACE BACKTEST arrays avec format Vertical
# TODO: CHECK LES GRAPHS
# NamedHorizontall: (une col par asset, une ligne par date, les noms d'asset sont les noms de colonnes)
# NameddVertical: (une col par date, une ligne par asset, + 1 col pour les noms d'asset)
# DatedData (jsplus le nom): le data de date et d'index stocké une fois seulement

# pour chaque version, mettre en place le categorical correspondant

# puis mettre en place long format (une col par attribut(return, date, nom), comme SQL ->
# array, categorical
# il faudra voir comment connecter le datedData

# au final, j'aurai un array filling, un base frame, et un categorical frame de chaque type:
# - vertical, horizontal, long