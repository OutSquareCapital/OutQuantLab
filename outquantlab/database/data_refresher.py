import yfinance as yf  # type: ignore
from pandas import DataFrame
from typing import NamedTuple
from outquantlab.metrics import pct_returns_np
from outquantlab.typing_conventions import DataFrameFloat

class AssetsData(NamedTuple):
    prices: DataFrameFloat
    returns: DataFrameFloat


def fetch_data(assets: list[str]) -> AssetsData:
    test_connection(asset=assets[0])
    return get_yf_data(assets=assets)


        
def get_yf_data(assets: list[str]) -> AssetsData:
    prices: DataFrameFloat = _get_prices_data(assets=assets)
    return AssetsData(
        prices=prices,
        returns=_get_returns_data(data=prices)
    )

def test_connection(asset: str) -> None:
    try:
        yf.Ticker(ticker=asset).history(period="1d")  # type: ignore
    except Exception as e:
        raise ConnectionError("Failed to connect to Yahoo Finance") from e

def _get_prices_data(assets: list[str]) -> DataFrameFloat:
    data: DataFrame | None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    return DataFrameFloat(data=data["Close"])  # type: ignore


def _get_returns_data(data: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(
        data=pct_returns_np(prices_array=data.get_array()),
        columns=data.columns,
        index=data.dates,
    )
