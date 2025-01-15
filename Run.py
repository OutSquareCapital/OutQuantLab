def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab(
            progress_callback=handle_progress
        )
    oql.execute_backtest()
    #graphs = GraphsCollection(stats=oql.stats)
    for metric, value in oql.stats.get_metrics():
        print(f"{metric}: {value}")

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from App import OutQuantLab
    #from Graphs import GraphsCollection
    print('OutQuantLab initialized')
    run()
    exit(0)