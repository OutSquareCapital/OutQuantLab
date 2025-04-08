from typing import NamedTuple, Protocol
from dataclasses import dataclass

@dataclass(slots=True)
class Asset:
    name: str
    active: bool


type ClustersTree = dict[str, list[str]]
type ClustersMap = dict[str, str]

class StrategyComponent(Protocol):
    name: str
    active: bool

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