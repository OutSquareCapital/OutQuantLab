import outquantlab as oql

def use_example() -> None:
    lab = oql.OutQuantLab(refresh_data=False)
    results: oql.BacktestResults = lab.run()
    lab.stats.overall.sharpe_ratio.plot(data=results.assets)
    lab.stats.rolling.drawdown.plot(data=results.portfolio, length=1250)
    lab.save_config()


if __name__ == "__main__":
    use_example()
