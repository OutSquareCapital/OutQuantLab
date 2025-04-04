import yfinance as yf  # type: ignore
from pandas import DataFrame

from outquantlab.structures import frames, arrays


def fetch_data(assets: list[str]) -> frames.DatedFloat:
    test_connection(asset=assets[0])
    return _get_yf_data(assets=assets)


def _get_yf_data(assets: list[str]) -> frames.DatedFloat:
    prices: frames.DatedFloat = _get_prices_data(assets=assets)
    return frames.DatedFloat(
        data=arrays.get_pct_returns(prices=prices.get_array()),
        columns=prices.columns,
        index=prices.get_index(),
    )


def test_connection(asset: str) -> None:
    try:
        yf.Ticker(ticker=asset).history(period="1d")  # type: ignore
    except Exception as e:
        raise ConnectionError("Failed to connect to Yahoo Finance") from e


def _get_prices_data(assets: list[str]) -> frames.DatedFloat:
    data: DataFrame | None = yf.download(  # type: ignore
        tickers=assets,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )
    if data is None:
        raise ValueError(f"No data returned from Yahoo Finance, from {assets}")
    return frames.DatedFloat.from_pandas(data=data["Close"])  # type: ignore
