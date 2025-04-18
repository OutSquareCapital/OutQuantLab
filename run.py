import outquantlab as oql


def internal_use() -> None:
    db = oql.DBStructure(db_name="data")
    tickers_data: oql.TickersData = db.tickers.get()
    # assets_config: oql.AssetsConfig = db.assets.get()
    indics_config: oql.IndicsConfig = db.indics.get()
    lab = oql.Backtestor(
        returns_df=tickers_data.get_returns_data(),
        indics=indics_config.get_indics_params(),
    )
    results = oql.PortfolioConstructor(
        data=lab.process_backtest(),
    )
    stats = oql.Stats()
    stats.equity.plot(data=results.assets, frequency=1)


def server_use() -> None:
    db = oql.DBStructure(db_name="data")
    tickers_data: oql.TickersData = db.tickers.get()
    # assets_config: oql.AssetsConfig = db.assets.get()
    indics_config: oql.IndicsConfig = db.indics.get()
    lab = oql.Backtestor(
        returns_df=tickers_data.get_returns_data(),
        indics=indics_config.get_indics_params(),
    )
    results = oql.PortfolioConstructor(
        data=lab.process_backtest())
    stats = oql.Stats()
    oql_server = oql.apis.LabServer()
    oql_server.store_result(
        data=stats.equity.get_formatted_data(data=results.assets, frequency=20)
    )
    oql_server.start_server()


def client_use() -> None:
    pass
    # client = oql.apis.LabClient()
    # data = client.request_data()
    # add data to db
    # process data
    # implementation to transform results.assets into a concrete futures position int
    # client.return_data(data=positions)


if __name__ == "__main__":
    server_use()
