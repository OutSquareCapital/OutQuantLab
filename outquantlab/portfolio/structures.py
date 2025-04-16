from typing import NamedTuple
from outquantlab.indicators import GenericIndic
import polars as pl

CLUSTERS_LEVELS: list[str] = [
    "assets",
    "indics",
    "params",
]

class ColumnName(NamedTuple):
    asset: str
    indic: str
    param: str

def get_categories(asset_names: list[str], indics: list[GenericIndic]) -> list[ColumnName]:
    return [
            ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.get_combo_names()
            for asset_name in asset_names
        ]

def get_categories_df(asset_names: list[str], indics: list[GenericIndic]) -> pl.DataFrame:

    data: list[dict[str, str]] = [
        {"assets": asset_name, "indics": indic.name, "params": param_name}
        for indic in indics
        for param_name in indic.get_combo_names()
        for asset_name in asset_names
    ]
    assets_categories = pl.Enum(categories=asset_names)
    indics_categories = pl.Enum(categories=[indic.name for indic in indics])
    schema = {
        "assets": assets_categories,
        "indics": indics_categories,
        "params": pl.Utf8,
    }
    return pl.DataFrame(data, schema=schema)