from concurrent.futures import ThreadPoolExecutor

from numpy import empty

from outquantlab.indicators import BaseIndic, DataArrays
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat, Float32


def get_signals_array(observations_nb: int, total_returns_streams: int) -> ArrayFloat:
    return empty(
        shape=(observations_nb, total_returns_streams),
        dtype=Float32,
    )


def calculate_portfolio_returns(
    returns_df: DataFrameFloat, grouping_levels: list[str]
) -> DataFrameFloat:
    return DataFrameFloat(
        data=returns_df.T.groupby(  # type: ignore
            level=grouping_levels, observed=True
        )
        .mean()
        .T
    )


def process_param(
    indic: BaseIndic, data_arrays: DataArrays, param_tuple: tuple[int, ...]
) -> ArrayFloat:
    return indic.execute(data_arrays, *param_tuple) * data_arrays.adjusted_returns_array


def process_indicator_parallel(
    indic: BaseIndic,
    data_arrays: DataArrays,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(
            indic=indic, data_arrays=data_arrays, param_tuple=param_tuple
        )

    return list(global_executor.map(process_single_param, indic.param_combos))
