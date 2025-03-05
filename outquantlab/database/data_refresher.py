import yfinance as yf  # type: ignore
from pandas import DataFrame

from outquantlab.metrics import pct_returns_np
from outquantlab.typing_conventions import DataFrameFloat


def get_yf_data(assets: list[str]) -> tuple[DataFrameFloat, DataFrameFloat]:
    prices_data: DataFrameFloat = _get_prices_data(assets=assets)
    returns_data: DataFrameFloat = _get_returns_data(prices_data=prices_data)

    return prices_data, returns_data


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
