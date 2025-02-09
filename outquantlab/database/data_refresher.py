from outquantlab.database.data_queries import DataQueries
from outquantlab.metrics import pct_returns_np
from outquantlab.typing_conventions import DataFrameFloat
from pandas import DataFrame
import yfinance as yf  # type: ignore


    
def refresh_yf_data(dbq: DataQueries, assets: list[str]) -> None:
    data: DataFrame | None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")
    else:
        prices_data = DataFrameFloat(data=data["Close"])  # type: ignore

        returns_data = DataFrameFloat(
            data=pct_returns_np(prices_array=prices_data.get_array()),
            columns=prices_data.columns,
            index=prices_data.dates,
        )
        
        assets_names: list[str] = prices_data.columns.to_list()

        dbq.select(file="price_data").save(data=prices_data)
        dbq.select(file="returns_data").save(data=returns_data)
        dbq.select(file="assets_names").save(data=assets_names)