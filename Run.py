
def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab(
            progress_callback=handle_progress, 
            database=DataBaseQueries()
        )
    oql.run_backtest()
    graph = oql.grphs.plot_stats_equity()
    graph.show() # type: ignore

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from App import OutQuantLab
    from DataBase import DataBaseQueries
    
    print('OutQuantLab initialized')
    run()
    exit(0)