from concurrent.futures import ThreadPoolExecutor
from outquantlab.indicators import BaseIndic
from outquantlab.typing_conventions import ArrayFloat, DataFrameFloat


def calculate_portfolio_returns(
    returns_df: DataFrameFloat, grouping_levels: list[str]
) -> DataFrameFloat:
    return DataFrameFloat(
        data=returns_df.T.groupby(level=grouping_levels, observed=True)  # type: ignore
        .mean()
        .T
    )


def process_param(indic: BaseIndic, param_tuple: tuple[int, ...]) -> ArrayFloat:
    return indic.execute(*param_tuple) * indic.data_arrays.adjusted_returns_array


def process_indicator_parallel(
    indic: BaseIndic,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(indic=indic, param_tuple=param_tuple)

    return list(global_executor.map(process_single_param, indic.param_combos))
