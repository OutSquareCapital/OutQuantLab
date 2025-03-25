def check_time() -> None:
    import time
    start: float = time.perf_counter()
    oql = OutQuantLab()
    oql.run()
    end: float = time.perf_counter()
    print(f"Backtest completed in {end - start:.2f} seconds.")

def test_app() -> None:
    oql = OutQuantLab(local=False)
    results = oql.run()
    print(results.portfolio)

if __name__ == "__main__":
    print("initializing OutQuantLab...")
    from outquantlab import OutQuantLab
    print("OutQuantLab initialized")
    test_app()
