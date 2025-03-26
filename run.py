def check_time() -> None:
    import time
    start: float = time.perf_counter()
    oql = OutQuantLab()
    oql.run()
    end: float = time.perf_counter()
    print(f"Backtest completed in {end - start:.2f} seconds.")

def test_app() -> None:
    oql = OutQuantLab()
    results = oql.run()
    oql.stats.correlation.plot(data=results.assets)
    oql.stats.rolling.drawdown.plot(data=results.portfolio, length=1250)
    oql.stats.overall.sharpe_ratio.plot(data=results.assets)
    oql.save_config()

if __name__ == "__main__":
    print("initializing OutQuantLab...")
    from outquantlab import OutQuantLab
    print("OutQuantLab initialized")
    test_app()
