import outquantlab as oql


def internal_use() -> None:
    dbp = oql.DataBaseProvider(db_name="data")
    config: oql.AppConfig = dbp.get_app_config()
    lab = oql.OutQuantLab(
        indics=config.indics_config.get_indics_params(),
        returns_df=dbp.get_returns_data(app_config=config, new_data=False),
    )
    results: oql.BacktestResults = lab.get_portfolio(data=lab.backtest())
    stats = oql.Stats()
    stats.equity.plot(data=results.portfolio, frequency=1)


def server_use() -> None:
    dbp = oql.DataBaseProvider(db_name="data")
    config: oql.AppConfig = dbp.get_app_config()
    lab = oql.OutQuantLab(
        indics=config.indics_config.get_indics_params(),
        returns_df=dbp.get_returns_data(app_config=config, new_data=False),
    )
    results: oql.BacktestResults = lab.get_portfolio(data=lab.backtest())
    stats = oql.Stats()
    oql_server = oql.apis.LabServer()
    oql_server.store_result(
        data=stats.equity.get_formatted_data(data=results.portfolio, frequency=20)
    )
    oql_server.start_server()


def client_use() -> None:
    client = oql.apis.LabClient()
    data = client.request_data()
    # add data to db
    # process data
    # implementation to transform results.assets into a concrete futures position int
    # client.return_data(data=positions)
    print(data)


if __name__ == "__main__":
    server_use()
