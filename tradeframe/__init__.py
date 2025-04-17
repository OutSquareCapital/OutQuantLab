from tradeframe.categorical import FrameCategorical, FrameCategoricalLong
from tradeframe.frames2d import FrameDated, FrameDefault, FrameMatrix
__all__: list[str] = [
    "FrameCategorical",
    "FrameCategoricalLong",
    "FrameDated",
    "FrameDefault",
    "FrameMatrix",
]

# TODO: FAIRE PIPELINE POUR LES 2 VERSIONS POSSIBLES:
# IndexedVertical: deja ok sauf pour la partie categorical (names horizontal, date vertical, une col par asset)
# IndexedHorizontal: a implementer pour la partie avant categorical (names vertical, date horiontal, une col par date)
# puis mettre en place long format (une col par attribut(return, date, nom), comme SQL
# fonctionne plus ou moins disons pour la partie categorical (meme si aucune implementation concrete)

# il faut que chacune soit implémentée dans chaque partie:
# db fetch/save
# base returns df
# array de backtest
# categorical df sur array
# backtest results 

# on ignore volontairement la partie plotting (deja implémentée pour IndexedVertical)