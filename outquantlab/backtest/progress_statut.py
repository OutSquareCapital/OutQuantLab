class ProgressStatus:
    def __init__(self) -> None:
        self.current_progress: int = 0

    def progress_callback(self, message: str) -> None:
        print(f"[{self.current_progress}%] {message}")

    def get_strategies_process_progress(
        self, indic_name: str, strategies_nb:int, signal_col_index: int, total_returns_streams: int
    ) -> None:
        self.current_progress = int(50 * signal_col_index / total_returns_streams)
        self.progress_callback(message=f"Processing {indic_name} with {strategies_nb} strategies...")

    def get_aggregation_progress(
        self, i: int, clusters_nb: int, current_lvl: str, columns_left: int
    ) -> None:
        self.current_progress = 50 + int(50 * (clusters_nb - i + 1) / clusters_nb)

        if self.current_progress == 100:
            self.progress_callback(message="Backtest Completed!")
        else:
            self.progress_callback(
                message=f"Aggregating {current_lvl}: {columns_left} columns left..."
            )
