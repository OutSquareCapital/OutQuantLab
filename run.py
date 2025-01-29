def launch_app() -> None:
    oql: OutQuantLab = OutQuantLab()
    oql.run()
    oql.graphs.plot_rolling_sharpe_ratio(returns_df=oql.data["lvl0"], length=252).show()  # type: ignore


if __name__ == "__main__":
    print("initializing OutQuantLab...")

    from sys import exit

    from outquantlab import OutQuantLab

    print("OutQuantLab initialized")
    launch_app()
    exit(0)
