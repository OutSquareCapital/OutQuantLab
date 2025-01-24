from concurrent.futures import ThreadPoolExecutor

from outquantlab.backtest.backtest_specs import BacktestSpecs
from outquantlab.indicators import BaseIndic
from outquantlab.typing_conventions import ArrayFloat, ProgressFunc


def process_param(indic: BaseIndic, param_tuple: tuple[int, ...]) -> ArrayFloat:
    return indic.execute(*param_tuple) * indic.returns_data.adjusted_returns_array


def process_indicator_parallel(
    indic: BaseIndic,
    global_executor: ThreadPoolExecutor,
) -> list[ArrayFloat]:
    def process_single_param(param_tuple: tuple[int, ...]) -> ArrayFloat:
        return process_param(indic=indic, param_tuple=param_tuple)

    return list(global_executor.map(process_single_param, indic.param_combos))


def fill_signals_array(
    signals_array: ArrayFloat,
    results: list[ArrayFloat],
    start_index: int,
    step: int,
) -> int:
    results_len: int = len(results)
    for i in range(results_len):
        end_index: int = start_index + step
        signals_array[:, start_index:end_index] = results[i]
        start_index = end_index

    return start_index


def process_strategies(
    indics_params: list[BaseIndic],
    backtest_specs: BacktestSpecs,
    progress_callback: ProgressFunc,
) -> ArrayFloat:
    signals_array: ArrayFloat = backtest_specs.get_signals_array()

    signal_col_index = 0
    with ThreadPoolExecutor(max_workers=backtest_specs.threads_nb) as global_executor:
        for indic in indics_params:
            try:
                results: list[ArrayFloat] = process_indicator_parallel(
                    indic=indic,
                    global_executor=global_executor,
                )

                signal_col_index: int = fill_signals_array(
                    signals_array=signals_array,
                    results=results,
                    start_index=signal_col_index,
                    step=backtest_specs.assets_count,
                )

                progress_callback(
                    int(100 * signal_col_index / backtest_specs.total_returns_streams),
                    f"Backtesting {indic.name}: {signal_col_index}/{backtest_specs.total_returns_streams}...",
                )
            except Exception as e:
                raise Exception(f"Error processing indicator {indic.name}: {e}")

    return signals_array
