from outquantlab import OutQuantLab

def use_example() -> None:
    oql = OutQuantLab(refresh_data=False)
    results = oql.run()
    oql.stats.overall.sharpe_ratio.plot(data=results.assets)
    oql.stats.rolling.drawdown.plot(data=results.portfolio, length=1250)
    oql.save_config()


if __name__ == "__main__":
    use_example()
