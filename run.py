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
    equity = stats.equity.get_formatted_data(data=results.portfolio, frequency=1)
    oql_server = oql.LabAPI()
    oql_server.send_result(data=equity)
    oql_server.start_server()

if __name__ == "__main__":
    server_use()
