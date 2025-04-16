from outquantlab.indicators import GenericIndic
from typing import NamedTuple, TypedDict
import numquant as nq
import polars as pl



class ColumnName(NamedTuple):
    asset: str
    indic: str
    param: str

class CategoriesDict(TypedDict):
    assets: str
    indics: str
    params: str

def get_categories_enum(names: list[str]) -> pl.Enum:
    return pl.Enum(categories=names)

def get_categories_dict_wide(asset_names: list[str], indics: list[GenericIndic]) -> list[CategoriesDict]:
    return [
        CategoriesDict(assets=asset_name, indics=indic.name, params=param_name)
        for indic in indics
        for param_name in indic.get_combo_names()
        for asset_name in asset_names
    ]

def get_categories_df_wide(data: list[CategoriesDict], asset_names: list[str], indic_names: list[str]
) -> pl.DataFrame:
    schema = {
        "assets": get_categories_enum(names=asset_names),
        "indics": get_categories_enum(names=indic_names),
        "params": pl.Utf8,
    }
    return pl.DataFrame(data=data, schema=schema)


def get_categories_list_long(asset_names: list[str], indics: list[GenericIndic]) -> list[ColumnName]:
    return [
            ColumnName(asset=asset_name, indic=indic.name, param=param_name)
            for indic in indics
            for param_name in indic.get_combo_names()
            for asset_name in asset_names
        ]

def get_categories_df_long(data: nq.Float2D, categories: list[ColumnName], asset_names: list[str], indic_names: list[str]) -> pl.DataFrame:
    index: nq.Int1D = nq.arrays.get_index(array=data)
    length: int = index.shape[0]
    result_frames: list[pl.DataFrame] = []
    asset_categories = get_categories_enum(names=asset_names)
    indic_categories = get_categories_enum(names=indic_names)
    for i, cat in enumerate(iterable=categories):
        df = pl.DataFrame(
            data={
                "index": pl.Series(name="index", values=index, dtype=pl.UInt32()),
                "return": pl.Series(
                    name="return", values=data[:, i], dtype=pl.Float32()
                ),
                "asset": pl.Series(name="asset", values=[cat.asset] * length, dtype=asset_categories),
                "indic": pl.Series(name="indic", values=[cat.indic] * length, dtype=indic_categories),
                "param": pl.Series(name="param", values=[cat.param] * length, dtype=pl.Categorical()),
            }
        )

        result_frames.append(df)

    return pl.concat(result_frames, rechunk=True)


