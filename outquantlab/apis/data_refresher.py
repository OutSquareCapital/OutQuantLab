import yfinance as yf  # type: ignore
from pandas import DataFrame

from outquantlab.structures import arrays, frames


def fetch_data(assets: list[str]) -> frames.DatedFloat:
    test_connection(asset=assets[0])
    data: frames.DatedFloat = _get_yf_data(assets=assets)
    check_data(data=data)
    return data

def check_data(data: frames.DatedFloat) -> None:
    base_shape: tuple[int, int] = data.shape
    data.clean_nans(axis=1)
    new_shape: tuple[int, int] = data.shape
    if base_shape != new_shape:
        raise ValueError(
            f"Deleted {base_shape[1] - new_shape[1]} columns after cleaning NaNs"
        )


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
