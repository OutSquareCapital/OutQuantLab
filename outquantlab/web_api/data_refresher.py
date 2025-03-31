import yfinance as yf  # type: ignore
from pandas import DataFrame
from outquantlab.metrics import pct_returns_np
from outquantlab.typing_conventions import DataFrameFloat

def fetch_data(assets: list[str]) -> DataFrameFloat:
    test_connection(asset=assets[0])
    return _get_yf_data(assets=assets)


        
def _get_yf_data(assets: list[str]) -> DataFrameFloat:
    prices: DataFrameFloat = _get_prices_data(assets=assets)
    return DataFrameFloat(
        data=pct_returns_np(prices_array=prices.get_array()),
        columns=prices.columns,
        index=prices.dates,
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
