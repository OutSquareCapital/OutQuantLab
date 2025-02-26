from outquantlab.database.data_queries import DataQueries
from outquantlab.metrics import pct_returns_np
from outquantlab.typing_conventions import DataFrameFloat
from pandas import DataFrame
import yfinance as yf  # type: ignore

def refresh_yf_data(dbq: DataQueries, assets: list[str]) -> None:
    prices_data: DataFrameFloat = _get_prices_data(assets=assets)
    returns_data: DataFrameFloat = _get_returns_data(prices_data=prices_data)
    _save_data(
        dbq=dbq, prices_data=prices_data, returns_data=returns_data
    )

def _get_prices_data(assets: list[str]) -> DataFrameFloat:
    data: DataFrame | None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if data is None:
        raise ValueError("Yahoo Finance Data Not Available")
    else:
        return DataFrameFloat(data=data["Close"])  # type: ignore


def _get_returns_data(prices_data: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(
        data=pct_returns_np(prices_array=prices_data.get_array()),
        columns=prices_data.columns,
        index=prices_data.dates,
    )


def _save_data(
    dbq: DataQueries, prices_data: DataFrameFloat, returns_data: DataFrameFloat
) -> None:
    assets_names: list[str] = prices_data.columns.to_list()

    dbq.select(file="price_data").save(data=prices_data)
    dbq.select(file="returns_data").save(data=returns_data)
    dbq.select(file="assets_names").save(data=assets_names)
