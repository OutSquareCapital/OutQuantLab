def launch_app() -> None:
    oql = OutQuantLab()
    print("running backtest...")
    oql.run()
    print(oql.data["lvl1"].mean(axis=0)*252*100) # type: ignore
    #oql.graphs.plot_rolling_sharpe_ratio(returns_df=oql.data["lvl0"], length=252).show()  # type: ignore


if __name__ == "__main__":
    print("initializing OutQuantLab...")

    from sys import exit

    from outquantlab import OutQuantLab

    print("OutQuantLab initialized")
    launch_app()
    exit(0)
