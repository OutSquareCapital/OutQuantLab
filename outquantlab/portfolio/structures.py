from typing import NamedTuple
from pandas import MultiIndex
from outquantlab.indicators import GenericIndic



CLUSTERS_LEVELS: list[str] = [
    "assets",
    "indics",
    "params",
]

class ColumnName(NamedTuple):
    asset: str
    indic: str
    param: str



def get_multi_index(asset_names: list[str], indics: list[GenericIndic]) -> MultiIndex:
    return MultiIndex.from_tuples(  # type: ignore
        tuples=get_categories(asset_names=asset_names, indics=indics),
        names=CLUSTERS_LEVELS,
    )

def get_categories(asset_names: list[str], indics: list[GenericIndic]) -> list[ColumnName]:
    return [
            ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.get_combo_names()
            for asset_name in asset_names
        ]