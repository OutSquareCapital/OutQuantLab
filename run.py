# type: ignore


def launch_app() -> None:
    print("running backtest...")
    start: float = time.perf_counter()
    oql = OutQuantLab()
    oql.run()
    end: float = time.perf_counter()
    print(f"Backtest completed in {end - start:.2f} seconds.")
    oql.save()
    test = oql.graphs.return_data(returns_df=oql.data['assets'])
    oql._dbp.save_backtest_results(result=test.data)


if __name__ == "__main__":
    print("initializing OutQuantLab...")

    from sys import exit

    from outquantlab import OutQuantLab
    import time
    print("OutQuantLab initialized")
    launch_app()
    exit(0)
