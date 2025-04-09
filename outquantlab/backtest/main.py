from concurrent.futures import ThreadPoolExecutor

from outquantlab.backtest.data import DataArrays
from outquantlab.backtest.specs import BacktestError, BacktestSpecs
from outquantlab.indicators import GenericIndic
from outquantlab.structures import arrays


class Backtestor:
    def __init__(self, pct_returns: arrays.Float2D, indics: list[GenericIndic]) -> None:
        self.indics: list[GenericIndic] = indics
        self.data: DataArrays = DataArrays(pct_returns=pct_returns)
        self.specs = BacktestSpecs(
            pct_returns=pct_returns,
            indics=self.indics,
        )

    def process_backtest(self) -> arrays.Float2D:
        main_array: arrays.Float2D = self.specs.get_main_array()
        with ThreadPoolExecutor(max_workers=self.specs.thread_nb) as global_executor:
            for indic in self.indics:
                try:
                    results_list: list[arrays.Float2D] = indic.process_params_parallel(
                        data_arrays=self.data,
                        global_executor=global_executor,
                    )

                    self.specs.fill_main_array(
                        main_array=main_array,
                        results_list=results_list,
                    )

                except Exception as e:
                    raise BacktestError(indic=indic, e=e)
        return main_array
