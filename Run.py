def handle_progress(progress: int, message: str) -> None:
    pass
    #print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab()
    import time
    total_time = 0
    start = time.perf_counter()
    iterations = 10
    for i in range(iterations):
        oql.execute_backtest(progress_callback=handle_progress)
        # add time
        end = time.perf_counter()
        time_elapsed = end - start
        total_time += time_elapsed
        print(f'{i}')
    avg_time = total_time / iterations
    print(f"Average time: {avg_time}")
    #graphs = GraphsCollection(stats=oql.stats)
    for metric, value in oql.stats.get_metrics().items():
        print(f"{metric}: {value}")

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from App import OutQuantLab
    #from Graphs import GraphsCollection
    print('OutQuantLab initialized')
    run()
    exit(0)