import outquantlab as oql


def use_example() -> None:
    dbp = oql.DataBaseProvider(db_name="data")
    config: oql.AppConfig = dbp.get_app_config()
    lab = oql.OutQuantLab(
        indics=config.indics_config.get_indics_params(),
        returns_df=dbp.get_returns_data(app_config=config, new_data=False),
    )
    strats: oql.arrays.Float2D = lab.backtest()
    results: oql.BacktestResults = lab.get_portfolio(data=strats)
    stats = oql.Stats()
    stats.overall.sharpe_ratio.plot(data=results.assets)
    stats.rolling.drawdown.plot(data=results.portfolio, length=1250)
    dbp.save_app_config(app_config=config)


if __name__ == "__main__":
    use_example()
