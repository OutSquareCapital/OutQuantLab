def handle_progress(progress: int, message: str) -> None:
    pass
    #print(f"[{progress}%] {message}")

def run() -> None:
    oql: OutQuantLab = OutQuantLab()
    import time
    total_time = 0
    iterations = 1
    for i in range(iterations):
        start = time.perf_counter()
        oql.execute_backtest(progress_callback=handle_progress)
        
        end = time.perf_counter()
        time_elapsed = end - start
        total_time += time_elapsed
        print(f'{i}')
    avg_time = total_time / iterations
    print(f"Average time: {avg_time}")
    #oql.save_all()
    graphs = GraphsCollection(stats=oql.stats)
    for metric, value in oql.stats.get_metrics().items():
        print(f"{metric}: {value}")

if __name__ == "__main__":

    print('initializing OutQuantLab...')

    from sys import exit
    from app import OutQuantLab
    from graphs import GraphsCollection
    print('OutQuantLab initialized')
    run()
    exit(0)