def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab()
    oql.execute_backtest(progress_callback=handle_progress)
    for metric, value in oql.stats.get_metrics().items():
        print(f"{metric}: {value}")
    oql.graphs.plot_stats_equity().show() # type: ignore
    oql.save_all()

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from outquantlab import OutQuantLab
    print('OutQuantLab initialized')
    run()
    exit(0)