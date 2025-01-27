def launch_app() -> None:
    oql: OutQuantLab = OutQuantLab()
    oql.run()


if __name__ == "__main__":
    print("initializing OutQuantLab...")

    from sys import exit

    from outquantlab import OutQuantLab

    print("OutQuantLab initialized")
    launch_app()
    exit(0)
