from outquantlab.backtest.data import DataArrays
from outquantlab.backtest.specs import BacktestSpecs, ThreadingManager
from outquantlab.indicators import GenericIndic, ParamResult
import numquant as nq
import tradeframe as tf
import polars as pl
from typing import TypedDict
from dataclasses import dataclass


class StrategyName(TypedDict):
    asset: str
    indic: str
    param: str


@dataclass(slots=True)
class RawResults:
    array: nq.Float2D
    strategies_names: list[StrategyName]
    schema: dict[str, pl.Enum | None]

    @property
    def gb_size(self) -> float:
        size: float = self.array.nbytes / (1024**3)
        return round(size, 2)
    
    def get_strategies_names_df(self) -> pl.DataFrame:
        return pl.DataFrame(
            data=self.strategies_names,
            schema=self.schema,
        )


class Backtestor:
    def __init__(
        self, returns_df: tf.FrameVertical, indics: list[GenericIndic]
    ) -> None:
        self.indics: list[GenericIndic] = indics
        self.asset_names: list[str] = returns_df.get_names()
        self.data: DataArrays = DataArrays(pct_returns=returns_df.get_array())
        self.schema = {
            "asset": pl.Enum(categories=self.asset_names),
            "indic": pl.Enum(categories=[indic.name for indic in self.indics]),
            "param": None,
        }

    def process_backtest(self) -> RawResults:
        specs = BacktestSpecs(pct_returns=self.data.pct_returns, indics=self.indics)
        strategie_names: list[StrategyName] = []
        threads: ThreadingManager = ThreadingManager()
        for indic in self.indics:
            try:
                results_list: list[ParamResult] = threads.process_params_parallel(
                    indic=indic,
                    params=indic.combos,
                    data_arrays=self.data,
                )
                specs.fill_main_array(
                    results_list=results_list,
                )
                for result in results_list:
                    names: list[StrategyName] = [
                        StrategyName(
                            asset=asset_name, indic=indic.name, param=result.param
                        )
                        for asset_name in self.asset_names
                    ]
                    strategie_names.extend(names)

            except Exception as e:
                raise Exception(
                    f"Error during backtest.\n Issue: {e} \n Indicator:\n {indic}"
                )
        return RawResults(
            array=specs.main_array,
            strategies_names=strategie_names,
            schema=self.schema,
        )

def get_categories_df_long(
    data: nq.Float2D,
    categories: list[StrategyName],
    asset_names: list[str],
    indic_names: list[str],
) -> pl.DataFrame:
    index: nq.Int1D = nq.arrays.get_index(array=data)
    length: int = index.shape[0]
    result_frames: list[pl.DataFrame] = []
    asset_categories = pl.Enum(categories=asset_names)
    indic_categories = pl.Enum(categories=indic_names)
    for i, cat in enumerate(iterable=categories):
        df = pl.DataFrame(
            data={
                "index": pl.Series(name="index", values=index, dtype=pl.UInt32()),
                "return": pl.Series(
                    name="return", values=data[:, i], dtype=pl.Float32()
                ),
                "asset": pl.Series(
                    name="asset", values=[cat["param"]] * length, dtype=asset_categories
                ),
                "indic": pl.Series(
                    name="indic", values=[cat["param"]] * length, dtype=indic_categories
                ),
                "param": pl.Series(name="param", values=[cat["param"]] * length),
            }
        )

        result_frames.append(df)

    return pl.concat(result_frames, rechunk=True)
