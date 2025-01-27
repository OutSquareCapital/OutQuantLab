class ProgressStatus:
    def __init__(self) -> None:
        self.current_progress: int = 0

    def progress_callback(self, message: str) -> None:
        print(f"[{self.current_progress}%] {message}")

    def get_strategies_process_progress(
        self, start_index: int, total_returns_streams: int
    ) -> None:
        self.current_progress = int(50 * start_index / total_returns_streams)
        self.progress_callback(message="Processing strategies...")

    def get_aggregation_progress(self, lvl: int, clusters_nb: int) -> None:
        self.current_progress = 50 + int(50 * (clusters_nb - lvl + 1) / clusters_nb)

        if self.current_progress == 100:
            self.progress_callback(message="Backtest Completed!")
        else:
            self.progress_callback(message="Aggregating returns...")
