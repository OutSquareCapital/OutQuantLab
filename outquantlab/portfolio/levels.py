from typing import NamedTuple
from outquantlab.indicators import BaseIndic
from pandas import MultiIndex

class AssetsClustersTuples(NamedTuple):
    cluster: str
    asset: str


class IndicsClustersTuples(NamedTuple):
    cluster: str
    indics: str
    params: str


class PortfolioClustersTuples(NamedTuple):
    assets_clusters: str
    assets: str
    indics_clusters: str
    indics: str
    params: str

CLUSTERS_LEVELS: list[str] = [
    "assets",
    "indics",
    "params",
]

class ColumnName(NamedTuple):
    asset: str
    indic: str
    param: str
    

def get_multi_index(asset_names: list[str], indics: list[BaseIndic]) -> MultiIndex:
    return MultiIndex.from_tuples(  # type: ignore
        tuples=[
            ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.params.get_combo_names()
            for asset_name in asset_names
        ],
        names=CLUSTERS_LEVELS
    )
