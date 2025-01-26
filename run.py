def run() -> None:
    oql: OutQuantLab = OutQuantLab()
    oql.run()
    print(oql.data_dfs.global_returns)
    oql.save_all()


if __name__ == "__main__":
    print("initializing OutQuantLab...")

    from sys import exit

    from outquantlab import OutQuantLab

    print("OutQuantLab initialized")
    run()
    exit(0)
