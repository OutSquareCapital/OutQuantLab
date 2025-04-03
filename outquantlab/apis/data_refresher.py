import yfinance as yf  # type: ignore
from pandas import DataFrame
from outquantlab.structures import DatedDataFrameFloat, pct_returns_array

def fetch_data(assets: list[str]) -> DatedDataFrameFloat:
    test_connection(asset=assets[0])
    return _get_yf_data(assets=assets)


        
def _get_yf_data(assets: list[str]) -> DatedDataFrameFloat:
    prices:DatedDataFrameFloat = _get_prices_data(assets=assets)
    return DatedDataFrameFloat(
        data=pct_returns_array(prices_array=prices.get_array()),
        columns=prices.columns,
        index=prices.get_index(),
    )

def test_connection(asset: str) -> None:
    try:
        yf.Ticker(ticker=asset).history(period="1d")  # type: ignore
    except Exception as e:
        raise ConnectionError("Failed to connect to Yahoo Finance") from e

def _get_prices_data(assets: list[str]) -> DatedDataFrameFloat:
    data: DataFrame | None = yf.download( #type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if data is None:
        raise ValueError(f"No data returned from Yahoo Finance, from {assets}")
    return DatedDataFrameFloat.from_pandas(data=data['Close']) # type: ignore
