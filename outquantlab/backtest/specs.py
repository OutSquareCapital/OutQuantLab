from os import cpu_count
from concurrent.futures import ThreadPoolExecutor
from outquantlab.indicators import GenericIndic, ParamResult, BaseParams
from outquantlab.backtest.data import DataArrays
import numquant as nq
from tqdm import tqdm


class ThreadingManager:
    def __init__(self) -> None:
        self.thread_nb: int = cpu_count() or 8
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=self.thread_nb)
    
    def process_params_parallel(
        self,
        indic: GenericIndic,
        params: list[BaseParams],
        data_arrays: DataArrays,
    ) -> list[ParamResult]:
        def process_single_param(param_tuple: BaseParams) -> ParamResult:
            return indic.process_single_param(
                data_arrays=data_arrays,
                param_tuple=param_tuple,
            )

        return list(self.executor.map(process_single_param, params))


class BacktestDimensions:
    def __init__(self, pct_returns: nq.Float2D, indics: list[GenericIndic]) -> None:
        self.assets: int = pct_returns.shape[1]
        self.days: int = pct_returns.shape[0]
        self.indics: int = len(indics)
        self.params: int = sum([indic.quantity for indic in indics])
        self.total: int = self.assets * self.params
        print(self.get_stats())

    def get_main_array(self) -> nq.Float2D:
        return nq.arrays.create_empty(length=self.days, width=self.total)

    def get_stats(self) -> str:
        return (
            f"Backtest Numbers Statistics:\n"
            f"  Days: {self.days}\n"
            f"  Assets: {self.assets}\n"
            f"  Indics: {self.indics}\n"
            f"  Params: {self.params}\n"
            f"  Total Nb of strategies: {self.total}\n"
        )


class BacktestSpecs:
    def __init__(self, pct_returns: nq.Float2D, indics: list[GenericIndic]) -> None:
        self._current_index: int = 0
        self.dimensions: BacktestDimensions = BacktestDimensions(
            pct_returns=pct_returns,
            indics=indics,
        )
        self.main_array: nq.Float2D = self.dimensions.get_main_array()
        self.progress_bar = tqdm(total=self.dimensions.total, desc="Backtest Progress")

    def fill_main_array(self, results_list: list[ParamResult]) -> None:
        for i in range(len(results_list)):
            end_index: int = self._current_index + self.dimensions.assets
            self.main_array[:, self._current_index : end_index] = results_list[i].data
            self._current_index = end_index
            self.update_progress(progress=self.dimensions.assets)

    def update_progress(self, progress: int) -> None:
        self.progress_bar.update(progress)
        self.progress_bar.refresh()
        if self._current_index >= self.dimensions.total:
            self.progress_bar.close()
