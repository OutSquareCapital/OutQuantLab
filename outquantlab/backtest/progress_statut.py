class ProgressStatus:
    def __init__(self, total_returns_streams: int, clusters_nb:int) -> None:
        self.current_progress: int = 0
        self.total_returns_streams: int = total_returns_streams
        self.clusters_nb: int = clusters_nb
    
    def progress_callback(self, message: str) -> None:
        print(f"[{self.current_progress}%] {message}")

    def get_strategies_process_progress(
        self, signal_col_index: int
    ) -> None:
        self.current_progress = int(50 * signal_col_index / self.total_returns_streams)
        self.progress_callback(message="Processing strategies...")

    def get_aggregation_progress(
        self, i: int
    ) -> None:
        self.current_progress = 50 + int(50 * (self.clusters_nb - i + 1) / self.clusters_nb)

        if self.current_progress == 100:
            self.progress_callback(message="Backtest Completed!")
        else:
            self.progress_callback(
                message="Aggregating returns..."
            )
