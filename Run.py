
def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab(
            progress_callback=handle_progress, 
            database=DataBaseQueries()
        )
    oql.run_backtest()
    graphs = GraphsCollection(stats=oql.stats)
    plot_fig = graphs.plot_overall_returns(True)
    plot_fig.show() # type: ignore

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from App import OutQuantLab
    from DataBase import DataBaseQueries
    from Graphs import GraphsCollection
    print('OutQuantLab initialized')
    run()
    exit(0)