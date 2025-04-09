from os import cpu_count

from outquantlab.indicators import GenericIndic
from outquantlab.structures import arrays
from tqdm import tqdm


class BacktestSpecs:
    def __init__(self, pct_returns: arrays.Float2D, indics: list[GenericIndic]) -> None:
        self.thread_nb: int = cpu_count() or 8
        self.current_index: int = 0
        self.assets: int = pct_returns.shape[1]
        self.days: int = pct_returns.shape[0]
        self.indics: int = len(indics)
        self.params: int = sum([indic.quantity for indic in indics])
        self.total: int = self.assets * self.params
        print(self.get_stats())
        self.progress_bar = tqdm(total=self.total, desc="Backtest Progress")

    def get_main_array(self) -> arrays.Float2D:
        return arrays.create_empty(length=self.days, width=self.total)

    def fill_main_array(
        self, main_array: arrays.Float2D, results_list: list[arrays.Float2D]
    ) -> None:
        for i in range(len(results_list)):
            end_index: int = self.current_index + self.assets
            main_array[:, self.current_index : end_index] = results_list[i]
            self.update_progress()
            self.current_index = end_index

    def update_progress(self) -> None:
        self.progress_bar.update(self.assets)
        self.progress_bar.refresh()
        if self.current_index >= self.total:
            self.progress_bar.close()

    def get_stats(self) -> str:
        return (
            f"Backtest Numbers Statistics:\n"
            f"  Threads: {self.thread_nb},\n"
            f"  Days: {self.days},\n"
            f"  Assets: {self.assets},\n"
            f"  Indics: {self.indics},\n"
            f"  Params: {self.params},\n"
            f"  Total Nb of strategies: {self.total}\n"
        )


class BacktestError(Exception):
    def __init__(
        self,
        indic: GenericIndic,
        e: Exception,
    ) -> None:
        super().__init__(f"Error during backtest.\n Issue: {e} \n Indicator:\n {indic}")
